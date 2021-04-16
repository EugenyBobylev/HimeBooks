from pathlib import Path
import pickle
from typing import Dict, List, Any

from app.models import Book

all_book_files: Dict = {}


def rename_book(old_book_path: str, new_book_name: str) -> bool:
    """
     Rename pdf book
    :param old_book_path: path and name of book with extension (.pdf)
    :param new_book_name: new name of book without extension (.pdf)
    :return: True when rename was made and new path of new book name with extension
    """
    result = False
    _old_book = Path(old_book_path)
    if _old_book.exists():
        _new_book = Path(_old_book.parent) / new_book_name
        _old_book.rename(_new_book)
        result = _new_book.exists()
    return result, str(_new_book)


def get_files():
    pdf_books: List[Any] = [el for lst in all_book_files.values() for el in lst]
    return pdf_books


def get_catalogs():
    return all_book_files.keys()


def find_pdf_files(catalog):
    """
    Get file name of pdf's files
    """
    pdf_files = [str(file) for file in Path(catalog).iterdir() if file.suffix == '.pdf']
    return pdf_files


def find_all_pdf_files():
    """
    Reload information about all pdf books
    """
    global all_book_files
    catalogs = all_book_files.keys()
    all_book_files = {}
    for catalog in catalogs:
        pdf_files = find_pdf_files(catalog)
        all_book_files[catalog] = pdf_files


def filter_exist_books(books: List[Book]):
    """
     Отфильтровать только существующие книги
    """
    filtered_books = None
    if books:
        filtered_books = [b for b in books if b.exists()]
    return filtered_books


def init(catalogs: List[str]):
    # dumpfn = str(Config.BASE_DIR) + '/app/static/config/all_books.pkl'
    all_books = []
    # if Path(dumpfn).exists():
    #    loaded_books = load(dumpfn)
    #    all_books = filter_exist_books(loaded_books)
    # else:
    init_filenames(catalogs)
    all_books = get_books()
    # dump(all_books, dumpfn)
    return all_books


def init_filenames(catalogs: List[str]):
    # TODO Сделать загрузку
    global all_book_files
    all_book_files = {}
    for catalog in catalogs:
        all_book_files[catalog] = ''
    find_all_pdf_files()


def create_book(path: str) -> Book:
    """
    Create instance of Book
    """
    book = Book(path)
    return book


def get_books():
    all_books = []
    files = get_files()
    for file_name in files:
        book: Book = create_book(file_name)
        all_books.append(book)
    return all_books


def dump(obj, fname):
    with open(fname, 'wb') as f:
        pickle.dump(obj, f)


def load(fname):
    obj = None
    with open(fname, 'rb') as f:
        obj = pickle.load(f)
    return obj


def paginate(full_data=None, page=None, per_page=None):
    filtered_data = None
    pagination = Pagination()
    if full_data:
        filtered_data = filter_exist_books(full_data)
    if filtered_data and page and per_page and page > 0 and per_page > 0:
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
        pagination.page = page if page <= pagination.pages else pagination.pages

    return pagination


class Pagination(object):
    has_next: bool = False
    has_prev: bool = False
    items = []              # the items for the current page
    next_num: int = None    # number of the next page
    page: int = None        # the current page number (1 indexed)
    pages: int = None       # the total number of pages
    per_page: int = None    # the number of items to be displayed on a page
    prev_num: int = None    # number of the previous page
    total: int = None       # the total number of items

    def iter_pages(self, left_edge=2, left_current=2, right_current=2, right_edge=2):
        if not self.items or len(self.items) == 0:
            return []
        _data = list(range(1, self.pages+1))
        result1 = set(_data[0:left_edge])
        left = self.page-left_current-1
        left = left if left > 0 else 0
        result2 = set(_data[left:self.page+right_current])
        left = self.pages - right_edge
        left = left if left > 0 else 0
        result3 = set(_data[left: self.pages])
        return list(result1.union(result2).union(result3))


if __name__ == '__main__':
    my_data = []
    paginator = paginate(my_data, 1, 12)
    paginator.iter_pages()
    print('*' * 100)
