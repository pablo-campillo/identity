from typing import TypeVar, Generic, List

T = TypeVar('T')

class Page(Generic[T]):
    items: List[T]
    page: int
    total: int
    has_next: bool

    def __init__(self, items: List[T], page: int, page_size: int, total: int):
        self.items = items
        self.page = page
        self.page_size = page_size
        self.total = total
        previous_items = (page - 1) * page_size
        self.has_next = previous_items + len(items) < total
