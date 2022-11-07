from typing import Generator, List, TypeVar

T = TypeVar('T')


def chunks(items: List[T], chunk_size: int) -> Generator[List[T], None, None]:
    """Yield successive chunks of a given size from a list of items"""
    if chunk_size <= 0:
        raise ValueError('Chunk size must be a positive integer')
    for i in range(0, len(items), chunk_size):
        start = i
        end = i + chunk_size
        yield items[start:end]
