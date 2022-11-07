from collections.abc import Generator
from typing import TypeVar

T = TypeVar('T')


def chunks(items: list[T], chunk_size: int) -> Generator[list[T], None, None]:
    """Yield successive chunks of a given size from a list of items"""
    if chunk_size <= 0:
        raise ValueError('Chunk size must be a positive integer')
    for i in range(0, len(items), chunk_size):
        start = i
        end = i + chunk_size
        yield items[start:end]
