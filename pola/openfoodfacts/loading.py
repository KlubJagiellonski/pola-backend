from __future__ import annotations

import csv
import gzip
import hashlib
import json
import os
import re
import tempfile
from collections.abc import Iterator
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path

from django.core.management.base import CommandError
from django.db import connection, transaction
from django.utils import timezone
from psycopg2.extras import execute_values

from pola.openfoodfacts.http import fetch_bytes, fetch_text
from pola.openfoodfacts.models import LoadRun

CSV_URL = 'https://static.openfoodfacts.org/data/en.openfoodfacts.org.products.csv.gz'
INDEX_URL = 'https://static.openfoodfacts.org/data/delta/index.txt'
DELTA_URL_PREFIX = 'https://static.openfoodfacts.org/data/delta/'
CSV_BASENAME = 'en.openfoodfacts.org.products.csv.gz'
MAX_DATABASE_BYTES = 25 * 1024**3
DELTA_NAME = re.compile(r'^openfoodfacts_products_(\d+)_(\d+)\.json\.gz$')
MISSING_CURSOR = (
    'No successful Open Food Facts load with a delta cursor. '
    'Run import_openfoodfacts_full by hand before the next delta sync.'
)
CHAIN_MISSED = 'The 14-day delta chain was missed. ' 'Run import_openfoodfacts_full by hand before the next delta sync.'

PRODUCT_COLUMNS = (
    'code',
    'product_name',
    'generic_name',
    'brands',
    'quantity',
    'brands_tags',
    'categories_tags',
    'countries_tags',
    'allergens_tags',
    'traces_tags',
    'ingredients_text',
    'nutriscore_grade',
    'nova_group',
    'ecoscore_grade',
    'completeness',
    'energy_kcal',
    'fat',
    'saturated_fat',
    'carbohydrates',
    'sugars',
    'fiber',
    'proteins',
    'salt',
    'image_url',
    'last_modified_t',
)

CSV_HEADERS = {
    'code': 'code',
    'product_name': 'product_name',
    'generic_name': 'generic_name',
    'brands': 'brands',
    'quantity': 'quantity',
    'brands_tags': 'brands_tags',
    'categories_tags': 'categories_tags',
    'countries_tags': 'countries_tags',
    'allergens_tags': 'allergens',
    'traces_tags': 'traces_tags',
    'ingredients_text': 'ingredients_text',
    'nutriscore_grade': 'nutriscore_grade',
    'nova_group': 'nova_group',
    'ecoscore_grade': 'ecoscore_grade',
    'completeness': 'completeness',
    'energy_kcal': 'energy-kcal_100g',
    'fat': 'fat_100g',
    'saturated_fat': 'saturated-fat_100g',
    'carbohydrates': 'carbohydrates_100g',
    'sugars': 'sugars_100g',
    'fiber': 'fiber_100g',
    'proteins': 'proteins_100g',
    'salt': 'salt_100g',
    'image_url': 'image_url',
    'last_modified_t': 'last_modified_t',
}

# The food CSV publishes allergens as text and does not include ecoscore_grade.
OPTIONAL_CSV_COLUMNS = {'ecoscore_grade'}

INTEGER_COLUMNS = {'nova_group', 'last_modified_t'}
INTEGER_LIMITS = {'nova_group': 2147483647, 'last_modified_t': 9223372036854775807}
DECIMAL_ABS_LIMIT = Decimal('1e10')
DECIMAL_COLUMNS = {
    'completeness',
    'energy_kcal',
    'fat',
    'saturated_fat',
    'carbohydrates',
    'sugars',
    'fiber',
    'proteins',
    'salt',
}
NUTRIENT_JSON_KEYS = {
    'energy_kcal': 'energy-kcal_100g',
    'fat': 'fat_100g',
    'saturated_fat': 'saturated-fat_100g',
    'carbohydrates': 'carbohydrates_100g',
    'sugars': 'sugars_100g',
    'fiber': 'fiber_100g',
    'proteins': 'proteins_100g',
    'salt': 'salt_100g',
}
TAG_COLUMNS = (
    'brands_tags',
    'categories_tags',
    'countries_tags',
    'allergens_tags',
    'traces_tags',
)


class DatabaseTooLarge(Exception):
    def __init__(self, size_bytes: int, limit_bytes: int) -> None:
        self.size_bytes = size_bytes
        self.limit_bytes = limit_bytes
        super().__init__(
            f'Database size {size_bytes} bytes would pass the {limit_bytes} byte limit. '
            'The live table was left in place.'
        )


@dataclass(frozen=True)
class DeltaFile:
    name: str
    start: int
    end: int

    @property
    def url(self) -> str:
        return DELTA_URL_PREFIX + self.name


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def parse_index(index_text: str) -> list[DeltaFile]:
    files: list[DeltaFile] = []
    for line in index_text.splitlines():
        name = line.strip()
        if not name:
            continue
        match = DELTA_NAME.match(name)
        if match is None:
            raise CommandError(f'Unexpected delta index line: {name}')
        files.append(DeltaFile(name=name, start=int(match.group(1)), end=int(match.group(2))))
    if not files:
        raise CommandError('Delta index is empty')
    files.sort(key=lambda item: (item.start, item.end, item.name))
    return files


def text_value(value: object) -> str | None:
    if value is None or isinstance(value, (list, dict)):
        return None
    text = str(value).replace('\x00', '').strip()
    return text or None


def tags_value(value: object) -> str | None:
    if isinstance(value, list):
        parts = [part for item in value if (part := text_value(item))]
        return ','.join(parts) or None
    return text_value(value)


def decimal_text(value: object) -> str | None:
    if value is None or isinstance(value, (list, dict)):
        return None
    text = str(value).strip()
    if text == '':
        return None
    try:
        number = Decimal(text)
    except InvalidOperation:
        return None
    if not number.is_finite() or abs(number) >= DECIMAL_ABS_LIMIT:
        return None
    return format(number, 'f')


def int_text(value: object, *, limit: int) -> str | None:
    if value is None or isinstance(value, (list, dict)):
        return None
    text = str(value).replace('\x00', '').strip()
    if text == '':
        return None
    try:
        number = Decimal(text)
    except InvalidOperation:
        return None
    if not number.is_finite():
        return None
    integer = int(number)
    if abs(integer) > limit:
        return None
    return str(integer)


def nutrient_value(document: dict[str, object], column: str) -> object:
    nutriments = document.get('nutriments')
    json_key = NUTRIENT_JSON_KEYS[column]
    if isinstance(nutriments, dict) and json_key in nutriments:
        return nutriments[json_key]
    return document.get(json_key)


def image_from_document(document: dict[str, object]) -> str | None:
    for key in ('image_url', 'image_front_url', 'image_front_small_url'):
        image = text_value(document.get(key))
        if image is not None:
            return image
    return None


def column_text(column: str, value: object) -> str | None:
    if column in INTEGER_COLUMNS:
        return int_text(value, limit=INTEGER_LIMITS[column])
    if column in DECIMAL_COLUMNS:
        return decimal_text(value)
    if column in TAG_COLUMNS:
        return tags_value(value)
    return text_value(value)


def row_from_csv(row: dict[str, str | None]) -> tuple[str | None, ...] | None:
    code = text_value(row.get('code'))
    if code is None:
        return None
    values: list[str | None] = []
    for column in PRODUCT_COLUMNS:
        if column == 'code':
            values.append(code)
            continue
        values.append(column_text(column, row.get(CSV_HEADERS[column])))
    return tuple(values)


def row_from_document(document: dict[str, object]) -> tuple[str | None, ...] | None:
    code = text_value(document.get('code'))
    if code is None:
        return None
    values: list[str | None] = []
    for column in PRODUCT_COLUMNS:
        if column == 'code':
            values.append(code)
        elif column == 'image_url':
            values.append(image_from_document(document))
        elif column in NUTRIENT_JSON_KEYS:
            values.append(column_text(column, nutrient_value(document, column)))
        else:
            values.append(column_text(column, document.get(column)))
    return tuple(values)


def encode_copy_field(value: str | None) -> str:
    if value is None:
        return r'\N'
    if value == r'\N' or any(char in value for char in ('\t', '\n', '\r', '"')):
        return '"' + value.replace('"', '""') + '"'
    return value


def encode_copy_row(values: tuple[str | None, ...]) -> bytes:
    line = '\t'.join(encode_copy_field(value) for value in values)
    return f'{line}\n'.encode()


class ProjectedCopy:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.row_count = 0
        self._handle: gzip.GzipFile | object | None = None
        self._pending = b''
        self._rows: Iterator[dict[str, str | None]] | None = None
        self._seen_codes: set[str] = set()

    def __enter__(self) -> ProjectedCopy:
        self._handle = _open_text(self.path)
        reader = csv.DictReader(self._handle, delimiter='\t')
        fieldnames = reader.fieldnames or []
        missing = [
            header
            for column, header in CSV_HEADERS.items()
            if column not in OPTIONAL_CSV_COLUMNS and header not in fieldnames
        ]
        if missing:
            raise CommandError('CSV is missing columns: ' + ', '.join(missing))
        self._rows = iter(reader)
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        if self._handle is not None:
            self._handle.close()

    def read(self, size: int = -1) -> bytes:
        if size is None or size < 0:
            size = 1024 * 1024
        while len(self._pending) < size:
            try:
                raw_row = next(self._rows)  # type: ignore[arg-type]
            except StopIteration:
                break
            projected = row_from_csv(raw_row)
            if projected is None or projected[0] is None or projected[0] in self._seen_codes:
                continue
            self._seen_codes.add(projected[0])
            self.row_count += 1
            self._pending += encode_copy_row(projected)
        chunk = self._pending[:size]
        self._pending = self._pending[size:]
        return chunk


def _open_text(path: Path) -> object:
    if path.suffix == '.gz':
        return gzip.open(path, 'rt', encoding='utf-8-sig', newline='')
    return path.open('rt', encoding='utf-8-sig', newline='')


def iter_documents(payload: str) -> Iterator[dict[str, object]]:
    stripped = payload.lstrip()
    if stripped == '':
        return
    if stripped[0] == '[':
        parsed = json.loads(stripped)
        if not isinstance(parsed, list):
            raise CommandError('Delta JSON array was not a list')
        for item in parsed:
            if not isinstance(item, dict):
                raise CommandError('Delta JSON array contains a non-object')
            yield item
        return
    for line_number, line in enumerate(payload.splitlines(), start=1):
        line = line.strip()
        if line == '':
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise CommandError(f'Invalid delta JSON on line {line_number}: {exc}') from exc
        if not isinstance(item, dict):
            raise CommandError(f'Delta line {line_number} is not an object')
        yield item


def database_size_bytes() -> int:
    with connection.cursor() as cursor:
        cursor.execute('SELECT pg_database_size(current_database())')
        return int(cursor.fetchone()[0])


def primary_key_name(table_name: str) -> str:
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT con.conname
            FROM pg_constraint con
            JOIN pg_class rel ON rel.oid = con.conrelid
            JOIN pg_namespace nsp ON nsp.oid = rel.relnamespace
            WHERE nsp.nspname = 'openfoodfacts'
              AND rel.relname = %s
              AND con.contype = 'p'
            ''',
            [table_name],
        )
        row = cursor.fetchone()
    if row is None:
        raise CommandError(f'openfoodfacts.{table_name} has no primary key')
    name = str(row[0])
    if re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', name) is None:
        raise CommandError(f'Unexpected primary key name on openfoodfacts.{table_name}')
    return name


def _record_run(
    *,
    started_at: object,
    mode: str,
    source_url: str,
    sha256: str | None,
    delta_end_unix: int | None,
    row_count: int | None,
    status: str,
    error: str | None,
) -> LoadRun:
    return LoadRun.objects.create(
        started_at=started_at,
        finished_at=timezone.now(),
        mode=mode,
        source_url=source_url,
        sha256=sha256,
        delta_end_unix=delta_end_unix,
        row_count=row_count,
        status=status,
        error=error,
    )


def _copy_sql() -> str:
    columns = ', '.join(PRODUCT_COLUMNS)
    return (
        f'COPY openfoodfacts.product_next ({columns}) FROM STDIN '
        "WITH (FORMAT csv, DELIMITER E'\\t', NULL '\\N', QUOTE '\"')"
    )


def _swap_tables() -> None:
    next_key = primary_key_name('product_next')
    with connection.cursor() as cursor:
        cursor.execute(f'ALTER TABLE openfoodfacts.product_next RENAME CONSTRAINT "{next_key}" TO product_live_pkey')
        cursor.execute('ALTER TABLE openfoodfacts.product RENAME TO product_old')
        cursor.execute('ALTER TABLE openfoodfacts.product_next RENAME TO product')
        cursor.execute('DROP TABLE openfoodfacts.product_old')
        cursor.execute('ALTER TABLE openfoodfacts.product RENAME CONSTRAINT product_live_pkey TO product_pkey')
        cursor.execute('CREATE TABLE openfoodfacts.product_next (LIKE openfoodfacts.product INCLUDING DEFAULTS)')
        cursor.execute('ALTER TABLE openfoodfacts.product_next ADD PRIMARY KEY (code)')


def import_full(
    *,
    csv_path: Path | None,
    index_path: Path | None,
    max_database_bytes: int,
) -> LoadRun:
    started_at = timezone.now()
    csv_file, index_file, downloaded = _resolve_full_inputs(csv_path, index_path)
    source_url = CSV_URL if downloaded else str(csv_file)
    actual_hash = file_sha256(csv_file)
    delta_files = parse_index(index_file.read_text(encoding='utf-8'))
    cursor_end = max(item.end for item in delta_files)
    try:
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute('TRUNCATE openfoodfacts.product_next')
            with ProjectedCopy(csv_file) as source:
                with connection.cursor() as cursor:
                    cursor.copy_expert(_copy_sql(), source)
                row_count = source.row_count
            if row_count == 0:
                raise CommandError('Full import contained no products. The live table was left in place.')
            size_bytes = database_size_bytes()
            if size_bytes > max_database_bytes:
                raise DatabaseTooLarge(size_bytes, max_database_bytes)
            _swap_tables()
            return _record_run(
                started_at=started_at,
                mode=LoadRun.Mode.FULL,
                source_url=source_url,
                sha256=actual_hash,
                delta_end_unix=cursor_end,
                row_count=row_count,
                status=LoadRun.Status.SUCCESS,
                error=None,
            )
    except DatabaseTooLarge as exc:
        _record_run(
            started_at=started_at,
            mode=LoadRun.Mode.FULL,
            source_url=source_url,
            sha256=actual_hash,
            delta_end_unix=None,
            row_count=None,
            status=LoadRun.Status.FAILED,
            error=str(exc),
        )
        raise CommandError(str(exc)) from exc


def download_directory() -> Path:
    configured = os.environ.get('OPENFOODFACTS_CACHE_DIR')
    directory = Path(configured) if configured else Path(tempfile.gettempdir()) / 'openfoodfacts'
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _resolve_full_inputs(
    csv_path: Path | None,
    index_path: Path | None,
) -> tuple[Path, Path, bool]:
    provided = (csv_path is not None, index_path is not None)
    if all(provided):
        return csv_path, index_path, False  # type: ignore[return-value]
    if any(provided):
        raise CommandError('Pass --csv and --index together, or pass none to download the official files.')
    directory = download_directory()
    csv_file = directory / CSV_BASENAME
    index_file = directory / 'index.txt'
    fetch_bytes(CSV_URL, csv_file)
    fetch_bytes(INDEX_URL, index_file, resume=False)
    return csv_file, index_file, True


def latest_cursor() -> int | None:
    run = (
        LoadRun.objects.filter(status=LoadRun.Status.SUCCESS)
        .exclude(delta_end_unix=None)
        .order_by('-finished_at', '-id')
        .first()
    )
    if run is None or run.delta_end_unix is None:
        return None
    return int(run.delta_end_unix)


def import_delta(*, index_path: Path | None, delta_dir: Path | None) -> list[LoadRun]:
    started_at = timezone.now()
    cursor = latest_cursor()
    if cursor is None:
        _record_run(
            started_at=started_at,
            mode=LoadRun.Mode.DELTA,
            source_url=INDEX_URL,
            sha256=None,
            delta_end_unix=None,
            row_count=None,
            status=LoadRun.Status.FAILED,
            error=MISSING_CURSOR,
        )
        raise CommandError(MISSING_CURSOR)
    if index_path is None:
        index_text = fetch_text(INDEX_URL)
    else:
        index_text = index_path.read_text(encoding='utf-8')
    delta_files = parse_index(index_text)
    oldest_start = min(item.start for item in delta_files)
    if cursor < oldest_start:
        _record_run(
            started_at=started_at,
            mode=LoadRun.Mode.DELTA,
            source_url=INDEX_URL,
            sha256=None,
            delta_end_unix=None,
            row_count=None,
            status=LoadRun.Status.FAILED,
            error=CHAIN_MISSED,
        )
        raise CommandError(CHAIN_MISSED)
    pending = [item for item in delta_files if item.end > cursor]
    if not pending:
        run = _record_run(
            started_at=started_at,
            mode=LoadRun.Mode.DELTA,
            source_url=INDEX_URL,
            sha256=None,
            delta_end_unix=cursor,
            row_count=0,
            status=LoadRun.Status.SUCCESS,
            error=None,
        )
        return [run]
    runs: list[LoadRun] = []
    for delta_file in pending:
        runs.append(_apply_delta_file(delta_file, delta_dir=delta_dir))
    return runs


def _apply_delta_file(delta_file: DeltaFile, *, delta_dir: Path | None) -> LoadRun:
    started_at = timezone.now()
    owned: tempfile.TemporaryDirectory[str] | None = None
    try:
        if delta_dir is None:
            owned = tempfile.TemporaryDirectory(prefix='openfoodfacts-delta-')
            path = Path(owned.name) / delta_file.name
            fetch_bytes(delta_file.url, path)
            source_url = delta_file.url
        else:
            path = delta_dir / delta_file.name
            if not path.is_file():
                raise CommandError(f'Missing delta file: {path}')
            source_url = str(path)
        digest = file_sha256(path)
        with gzip.open(path, 'rt', encoding='utf-8') as handle:
            documents = list(iter_documents(handle.read()))
        rows = []
        for document in documents:
            projected = row_from_document(document)
            if projected is not None:
                rows.append(_adapt_row(projected))
        with transaction.atomic():
            if rows:
                _upsert_rows(rows)
            return _record_run(
                started_at=started_at,
                mode=LoadRun.Mode.DELTA,
                source_url=source_url,
                sha256=digest,
                delta_end_unix=delta_file.end,
                row_count=len(rows),
                status=LoadRun.Status.SUCCESS,
                error=None,
            )
    except Exception as exc:
        _record_run(
            started_at=started_at,
            mode=LoadRun.Mode.DELTA,
            source_url=delta_file.url,
            sha256=None,
            delta_end_unix=None,
            row_count=None,
            status=LoadRun.Status.FAILED,
            error=str(exc),
        )
        raise
    finally:
        if owned is not None:
            owned.cleanup()


def _adapt_row(values: tuple[str | None, ...]) -> tuple[object, ...]:
    adapted: list[object] = []
    for column, value in zip(PRODUCT_COLUMNS, values):
        if value is None:
            adapted.append(None)
        elif column in INTEGER_COLUMNS:
            adapted.append(int(value))
        elif column in DECIMAL_COLUMNS:
            adapted.append(Decimal(value))
        else:
            adapted.append(value)
    return tuple(adapted)


def _upsert_rows(rows: list[tuple[object, ...]]) -> None:
    columns = ', '.join(PRODUCT_COLUMNS)
    assignments = ', '.join(f'{column} = EXCLUDED.{column}' for column in PRODUCT_COLUMNS if column != 'code')
    statement = (
        f'INSERT INTO openfoodfacts.product ({columns}) VALUES %s ON CONFLICT (code) DO UPDATE SET {assignments}'
    )
    with connection.cursor() as cursor:
        execute_values(cursor, statement, rows, page_size=1000)
