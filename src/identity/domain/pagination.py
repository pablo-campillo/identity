from typing import TypeVar, Generic, List

T = TypeVar('T')

class Page(Generic[T]):
    """Generic class that represents a paginated result

    :param items: List of objects
    :type items: List[T]
    :param page: Page number of the items. First page is 1
    :type page: int
    :param total: Total number of object
    :type total: int
    :param has_next: `True` if there are more objects, `False` otherwise
    :type has_next: bool
    """
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
