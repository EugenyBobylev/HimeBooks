from pathlib import Path
from typing import Dict, List, Any

from app import bookspdf

all_books: Dict = {}


def get_books():
    pdf_books: List[Any] = [el for lst in all_books.values() for el in lst]
    return pdf_books


def get_catalogs():
    return all_books.keys()


def get_catalog_books(catalog):
    """
    Get file name of pdf's files
    """
    pdf_books = [str(file) for file in Path(catalog).iterdir() if file.suffix == '.pdf']
    return pdf_books


def init_all_books():
    """
    Reload information about all pdf books
    """
    global all_books
    catalogs = all_books.keys()
    all_books = {}
    for catalog in catalogs:
        pdf_books = get_catalog_books(catalog)
        all_books[catalog] = pdf_books


def init():
    all_books['/home/bobylev/Downloads/Books/'] = ''
    all_books['/media/bobylev/Data/Downloads/Telegram Desktop/'] = ''
    init_all_books()


def paginate(full_data=None, page=None, per_page=None):
    pagination = Pagination()
    if full_data and page and per_page and page > 0 and per_page > 0:
        pagination.page = page
        pagination.per_page = per_page

        first = (page-1) * per_page
        last = first + per_page
        pagination.items = full_data[first:last]
        pagination.total = len(full_data)
        pagination.pages = int(pagination.total / per_page) + (1 if pagination.total % per_page else 0)
        pagination.has_next = (page < pagination.pages)
        pagination.has_prev = (page > 1)
        pagination.next_num = page + 1 if pagination.has_next else page
        pagination.prev_num = page - 1 if pagination.has_prev else page

    return pagination


class Pagination(object):
    has_next: bool = False
    has_prev: bool = False
    items = []            # the items for the current page
    next_num: int = None    # number of the next page
    page: int = None        # the current page number (1 indexed)
    pages: int = None       # the total number of pages
    per_page: int = None    # the number of items to be displayed on a page
    prev_num: int = None    # number of the previous page
    total: int = None       # the total number of items

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        page_items = []
        if self.page >= left_edge:
            page_items = list(range(1, left_edge + 1))
        else:
            page_items = list(range(1, self.page + 1))
        if self.page >

        return page_items


if __name__ == '__main__':
    # init()
    # books = get_books()
    # print(len(books))
    # print(books)
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    p1 = paginate(data, 1, 5)
    p2 = paginate(data, 2, 5)
    p3 = paginate(data, 3, 4)
    p9 = paginate(data, 9, 5)
    p1_1 = paginate(data, 1, 100)
    print(p1.items)
    print(p2.items)
    print(p3.items)
    print(p9.items)
    print(p1_1.items)

    print(paginate(None, 1, 10).items)
    print(paginate(data, 0, 10).items)
    print(paginate(None, None, None).items)
    print(paginate(data, 1, None).items)
