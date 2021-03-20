import os
from flask import redirect, render_template, request, url_for

from app import app
from app.models import Catalog
import app.bookspdf as pdf

ROWS_PER_PAGE = 5

all_books = []
if not all_books:
    pdf.init()
    all_books = pdf.get_books()
    print(len(all_books))


@app.route('/')
@app.route('/index')
@app.route('/page/<int:page>')
@app.route('/index/page/<int:page>')
def index(page=1):
    page = request.args.get('page', page, type=int)
    page_books = pdf.paginate(all_books, page=page, per_page=ROWS_PER_PAGE)
    for book in page_books.items:
        book.set_cover()
    return render_template('index.html', books=page_books)


@app.route('/book')
def open_book():
    path = request.args.get('path')
    page = request.args.get('page')
    os.popen(f'okular "{path}"')
    return redirect(url_for('index', page=page))


@app.route('/settings')
def settings():
    catalogs = Catalog.query.all()
    return render_template('settings.html', catalogs=catalogs)


@app.route('/addcatalog')
def add_catalog():
    catalog = request.args.get('catalog')
    print(str(catalog))
    return redirect(url_for('settings'))


@app.route('/updatecatalogs')
def update_catalogs():
    return redirect(url_for('settings'))
