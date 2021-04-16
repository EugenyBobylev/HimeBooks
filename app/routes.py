import os
import re

from flask import redirect, render_template, request, url_for, make_response

from app import app
import app.bookspdf as pdf
import app.iniconfig as cfg

ROWS_PER_PAGE = 12
COOKIE_SEARCH = 'search'

all_books = []   # все книги
books = []       # все отфильтрованные книги

if not all_books:
    catalogs = cfg.read_paths()
    all_books = pdf.init(catalogs)
    books = all_books.copy()


def change_renamed_book(old_book, new_book):
    """
    Заменить переименованную книгу во всех коллекциях
    :param old_book: книга со старым наименованием
    :param new_book: переименованная кника
    """
    idx = all_books.index(old_book)
    all_books[idx] = new_book

    idx = books.index(old_book)
    books[idx] = new_book


def filter_books(search_value: str):
    _books = []
    if search_value and search_value != '':
        _books = [book for book in all_books if book.name.lower().find(search_value.lower()) >= 0]
    else:
        _books = all_books.copy()
    print('Oooooooppppsssss!!!!')
    return _books


@app.route('/')
@app.route('/index')
@app.route('/page/<int:page>')
@app.route('/index/page/<int:page>')
def index(page=1):
    page = request.args.get('page', page, type=int)
    search_value = request.cookies.get(COOKIE_SEARCH) if request.cookies.get(COOKIE_SEARCH) else ''
    if search_value:
        global books
        books = filter_books(search_value)
    page_books: pdf.Pagination = pdf.paginate(books, page=page, per_page=ROWS_PER_PAGE)
    for book in page_books.items:
        book.set_cover()
    return render_template('index.html', books=page_books, search_value=search_value)


@app.route('/book')
def open_book():
    path = request.args.get('path')
    page = request.args.get('page')
    if path:
        os.popen(f'okular "{path}"')
    return redirect(url_for('index', page=page))


@app.route('/settings')
def settings():
    _catalogs = cfg.read_paths()
    print(_catalogs)
    return render_template('settings.html', catalogs=_catalogs)


@app.route('/addcatalog')
def add_catalog():
    catalog = request.args.get('catalog')
    print(str(catalog))
    return redirect(url_for('settings'))


@app.route('/updatecatalogs')
def update_catalogs():
    return redirect(url_for('settings'))


def get_book_path(href) -> str:
    """
     get book.pdf path from href
    """
    book_path = ''
    match = re.search('path=(.*)', href)
    if match:
        book_path = match.group(1)
    return book_path


@app.route('/delete/<name>')
def delete_book(name):
    name = request.args.get('name', name, type=str)
    book = [book for book in books if book.name == name][0]

    idx = books.index(book) + 1  # because pages count from 1
    per_page = ROWS_PER_PAGE
    page = int(idx / per_page) + (1 if idx % per_page else 0)

    all_books.remove(book)
    books.remove(book)

    print(f'page:{page}, idx:{idx}, per_page:{per_page}, delete book: "{book.name}"')
    # return '', 204
    return redirect(url_for('index', page=page))


@app.route('/rename', methods=['POST'])
def rename_book(name=''):
    data = request.get_json()
    book_href = data["book_href"]
    book_name = data["book_name"]
    book_name += '.pdf'
    book_path = get_book_path(book_href)
    if book_path:
        book = [book for book in books if book.pdf == book_path][0]
        result = pdf.rename_book(book_path, book_name)
        ok = result[0]
        if ok:
            renamed_book_path = result[1]
            renamed_book = pdf.create_book(renamed_book_path)

            idx = all_books.index(book)
            all_books[idx] = renamed_book

            idx = books.index(book)
            books[idx] = renamed_book
    return renamed_book_path, 200


@app.route('/tagschanged', methods=['POST'])
def tags_changed():
    data = request.get_json()
    book_href = data["book_href"]
    book_tags = data["book_tags"]
    book_path = get_book_path(book_href)
    if book_path:
        book = [book for book in all_books if book.pdf == book_path][0]
        book.set_tags(book_tags)
    return '', 204


@app.route('/findbooks', methods=['POST'])
def find_books():
    part = request.form['part']
    filtered_books = filter_books(part)
    if len(filtered_books) < 1:
        return '', 204
    global books
    books = filtered_books
    res = make_response(redirect('/index'))
    res.set_cookie(COOKIE_SEARCH, part)
    return res


@app.route('/resetsearch')
def reset_search_books():
    global books
    books = filter_books('')
    res = make_response('/index')
    if request.cookies.get(COOKIE_SEARCH):
        res.set_cookie(COOKIE_SEARCH, '', max_age=0)
    return res
