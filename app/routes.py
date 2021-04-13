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


@app.route('/')
@app.route('/index')
@app.route('/page/<int:page>')
@app.route('/index/page/<int:page>')
def index(page=1):
    print("execute index()")
    page = request.args.get('page', page, type=int)
    search_value = request.cookies.get(COOKIE_SEARCH) if request.cookies.get(COOKIE_SEARCH) else ''
    print(f'page={page}')
    page_books: pdf.Pagination = pdf.paginate(books, page=page, per_page=ROWS_PER_PAGE)
    for book in page_books.items:
        book.set_cover()
        print(f'name="{book.book_name}"')
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


# @app.route('/rename/<name>')
@app.route('/rename', methods=['POST'])
def rename_book(name=''):
    data = request.get_json()
    book_href = data["book_href"]
    book_name = data["book_name"]
    book_name += '.pdf'
    book_path = get_book_path(book_href)
    if book_path:
        book = [book for book in books if book.pdf_name == book_path][0]
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
        book = [book for book in all_books if book.pdf_name == book_path][0]
        book.set_tags(book_tags)
    return '', 204


@app.route('/findbooks', methods=['POST'])
def find_books():
    part = request.form['part']
    res = make_response(redirect('/index?pge=1'))
    global books
    if part and part != '':
        filtered_books = [book for book in all_books if book.book_name.lower().find(part.lower()) >= 0]
        if len(filtered_books) > 0:
            books = filtered_books.copy()
            res.set_cookie(COOKIE_SEARCH, part)
        else:
            print('Книги не найдены')
            return '', 204
    else:
        books = all_books.copy()
        res.set_cookie(COOKIE_SEARCH, part, max_age=0)
    #  return redirect('/index?pge=1')
    return res


@app.route('/resetsearch')
def reset_search_books():
    global books
    books = all_books.copy()
    res = make_response('/index')
    if request.cookies.get(COOKIE_SEARCH):
        res.set_cookie(COOKIE_SEARCH, '', max_age=0)

    return res
