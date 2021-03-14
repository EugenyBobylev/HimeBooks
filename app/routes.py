import os

from flask import redirect, render_template, request, url_for
from app import app
from app.models import Book

ROWS_PER_PAGE = 5


@app.route('/')
@app.route('/index')
@app.route('/page/<int:page>')
@app.route('/index/page/<int:page>')
def index(page=1):
    page = request.args.get('page', page, type=int)
    books = Book.query.paginate(page=page, per_page=ROWS_PER_PAGE)
    for book in books.items:
        book.set_cover()
    return render_template('index.html', books=books)


@app.route('/book')
def open_book():
    path = request.args.get('path')
    page = request.args.get('page')
    print(path)
    print(page)
    os.popen(f'okular "{path}"')
    return redirect(url_for('index', page=page))
