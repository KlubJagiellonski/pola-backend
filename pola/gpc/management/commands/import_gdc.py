import argparse
import itertools
import xml.etree.ElementTree as ET
from functools import cached_property
from typing import Any, NamedTuple

from django.core.management import BaseCommand
from tqdm import tqdm

from pola.collection_utils import chunks
from pola.gpc.models import GPCBrick, GPCClass, GPCFamily, GPCSegment
from pola.management.command_utils import ask_yes_no

IMPORT_TYPES_ORDER = [GPCSegment, GPCFamily, GPCClass, GPCBrick]
IMPORT_TYPE_NAMES_ORDER = [d.__name__ for d in IMPORT_TYPES_ORDER]
IMPORT_TYPES_MAP = {k.__name__: k for k in IMPORT_TYPES_ORDER}
IMPORT_PARENTS = {
    k: (v if v is None else IMPORT_TYPES_MAP.get(v))
    for k, v in itertools.zip_longest(IMPORT_TYPE_NAMES_ORDER, [None, *IMPORT_TYPE_NAMES_ORDER])
}


def normalize_boolean(v):
    if v is None:
        return None
    if v == '':
        return None
    if v.lower() == 'true':
        return True
    if v.lower() == 'false':
        return True
    raise TypeError(f"Unexpected value: {v}")


def normalize_string(v):
    if v is None:
        return None
    if not isinstance(v, str):
        raise TypeError(f"Unexpected type: {type(v)}")
    if v == '':
        return None
    if len(v.strip()) == 0:
        return None
    return v.strip()


class GDCImportPlan(NamedTuple):
    to_add: list[tuple[type, dict[str, Any]]]
    to_update: list[tuple[type, dict[str, Any]]]

    def __repr__(self):
        return (
            f"To add count: {len(self.to_add)}\n"
            f"To update count: {len(self.to_update)}\n"
            f"To add by type: {self.counts_to_add_by_type}\n"
            f"To update by type: {self.counts_to_update_by_type}"
        )

    @property
    def counts_to_add_by_type(self) -> dict[str, int]:
        sorted_list = sorted(self.to_add, key=lambda d: d[0].__name__)
        return {k: len(list(g)) for k, g in itertools.groupby(sorted_list, lambda d: d[0].__name__)}

    @property
    def counts_to_update_by_type(self) -> dict[str, int]:
        sorted_list = sorted(self.to_update, key=lambda d: d[0].__name__)
        return {k: len(list(g)) for k, g in itertools.groupby(sorted_list, lambda d: d[0].__name__)}


class GDCImportPlanner:
    def __init__(self, document, output):
        assert document.tag == 'schema'
        self._schema = document
        self._output = output
        self._current_plan = None
        self._entities_cache = {}

    @cached_property
    def total_element_count(self):
        return (
            sum(1 for _ in self._schema)
            + sum(1 for segment in self._schema for _ in segment)
            + sum(1 for segment in self._schema for family in segment for _ in family)
            + sum(1 for segment in self._schema for family in segment for class_ in family for _ in class_)
        )

    def _get_entity_cache(self, entity_type, lookup_key):
        cache_key = (lookup_key, entity_type.__name__)
        entity_cache = self._entities_cache.get(cache_key)
        if entity_cache is None:
            entity_cache = {getattr(s, lookup_key): s for s in entity_type.objects.all()}
            self._entities_cache[cache_key] = entity_cache
        return entity_cache

    def start(self):
        self._current_plan = GDCImportPlan(to_add=[], to_update=[])

        with tqdm(total=self.total_element_count, file=self._output, unit="el") as self.pbar:
            for segment in self._schema:
                assert segment.tag == 'segment'
                self._process_segment(segment)
            self.pbar.update(1)
        # Free resources
        self._entities_cache = {}
        return self._current_plan

    def _process_segment(self, segment):
        segment_attr = dict(
            code=(normalize_string(segment.attrib['code'])),
            text=normalize_string(segment.attrib['text']),
            definition=normalize_string(segment.attrib['definition']),
            active=normalize_boolean(segment.attrib['active']),
        )
        self._plan_create_or_update_entity(GPCSegment, segment_attr)

        for family in segment:
            assert family.tag == 'family'
            self._process_family(segment, family)
        self.pbar.update(1)

    def _process_family(self, parent, family):
        segment_attr = dict(
            code=(normalize_string(family.attrib['code'])),
            text=normalize_string(family.attrib['text']),
            definition=normalize_string(family.attrib['definition']),
            active=normalize_boolean(family.attrib['active']),
            parent_code=parent.attrib['code'],
        )
        self._plan_create_or_update_entity(GPCFamily, segment_attr)

        for class_ in family:
            assert class_.tag == 'class'
            self._process_class(family, class_)
        self.pbar.update(1)

    def _process_class(self, parent, class_):
        class_attr = dict(
            code=(normalize_string(class_.attrib['code'])),
            text=normalize_string(class_.attrib['text']),
            definition=normalize_string(class_.attrib['definition']),
            active=normalize_boolean(class_.attrib['active']),
            parent_code=parent.attrib['code'],
        )
        self._plan_create_or_update_entity(GPCClass, class_attr)

        for brick in class_:
            assert brick.tag == 'brick'
            self._process_brick(class_, brick)
        self.pbar.update(1 + len(class_))

    def _process_brick(self, parent, brick):
        brick_attr = dict(
            code=(normalize_string(brick.attrib['code'])),
            text=normalize_string(brick.attrib['text']),
            definition=normalize_string(brick.attrib['definition']),
            definitionExcludes=normalize_string(brick.attrib.get('definitionExcludes')),
            active=normalize_boolean(brick.attrib['active']),
            parent_code=parent.attrib['code'],
        )
        self._plan_create_or_update_entity(GPCBrick, brick_attr)

    def _plan_create_or_update_entity(self, entity_type, entity_attr):
        entity_cache = self._get_entity_cache(entity_type, 'code')

        existing_entity = entity_cache.get(entity_attr['code'])
        if existing_entity:
            diff_attrs = {}
            for k, v in entity_attr.items():
                if k == "parent_code":
                    parent_entity_type = IMPORT_PARENTS.get(entity_type.__name__)
                    parent_entity = self._get_entity_cache(parent_entity_type, 'id').get(existing_entity.parent_id)
                    attr_value = parent_entity.code
                else:
                    attr_value = getattr(existing_entity, k)
                if attr_value != v:
                    diff_attrs[k] = v
            if diff_attrs:
                self._current_plan.to_update.append((entity_type, entity_attr))
        else:
            self._current_plan.to_add.append((entity_type, entity_attr))


class GDCImportPlanExecutor:
    def __init__(self, output, chunk_size=100):
        self._output = output
        self._entities_cache = {}
        self.chunk_size = chunk_size

    def _get_entity_cache(self, entity_type, lookup_key):
        cache_key = (lookup_key, entity_type.__name__)
        entity_cache = self._entities_cache.get(cache_key)
        if entity_cache is None:
            entity_cache = {getattr(s, lookup_key): s for s in entity_type.objects.all()}
            self._entities_cache[cache_key] = entity_cache
        return entity_cache

    def start(self, plan: GDCImportPlan):
        sorted_plan_by_type = [
            (entity_name, [entity_attrs for _, entity_attrs in to_add_entry])
            for entity_name, to_add_entry in itertools.groupby(
                sorted(plan.to_add, key=lambda d: IMPORT_TYPE_NAMES_ORDER.index(d[0].__name__)),
                key=lambda d: d[0].__name__,
            )
        ]
        total_new_entities = sum(len(entity_attrs) for _, entity_attrs in plan.to_add)
        if total_new_entities:
            self._output.write(f"Creating a new {total_new_entities} entities:")
            with tqdm(total=total_new_entities, file=self._output, unit="el") as self.pbar:
                for entity_name, entities_attr_list in sorted_plan_by_type:
                    self._process_entity_type(entities_attr_list, entity_name)
        total_updated_entities = sum(len(entity_attrs) for _, entity_attrs in plan.to_update)
        if total_updated_entities:
            raise Exception("Not implemented")

    def _process_entity_type(self, entities_attr_list, entity_name):
        self.pbar.set_description(f"Saving {entity_name}")
        entity_type = IMPORT_TYPES_MAP.get(entity_name)
        parent_entity_type = IMPORT_PARENTS.get(entity_name)
        for chunk in chunks(entities_attr_list, self.chunk_size):
            to_create_entities = []
            for entity_attrs in chunk:
                new_entity_attrs = {}
                for k, v in entity_attrs.items():
                    if k == 'parent_code':
                        parent_entity_by_code = self._get_entity_cache(parent_entity_type, 'code')
                        k = 'parent_id'
                        v = parent_entity_by_code.get(v).id
                    new_entity_attrs[k] = v
                new_entity = entity_type(**new_entity_attrs)
                to_create_entities.append(new_entity)

            entity_type.objects.bulk_create(to_create_entities)
            self.pbar.update(len(chunk))


class Command(BaseCommand):
    help = 'Import GDC data from .xml file'

    def add_arguments(self, parser):
        parser.add_argument('xml_filepath', type=argparse.FileType(mode='r', encoding='UTF-8'))
        parser.add_argument(
            '--noinput',
            '--no-input',
            action='store_false',
            dest='interactive',
            help='Tells Django to NOT prompt the user for input of any kind. ',
        )

    def handle(self, *args, **options):
        with options['xml_filepath'] as xml_file:
            root = ET.fromstring(xml_file.read())

        importer = GDCImportPlanner(document=root, output=self.stderr)
        plan = importer.start()
        if options['interactive'] and not ask_yes_no(f'Prepared plan \n{repr(plan)}\n. Proceed? (Y/n)'):
            self.stdout.write(self.style.ERROR('Operation cancelled.'))
            return
        executor = GDCImportPlanExecutor(output=self.stderr)
        executor.start(plan)
