from flask import render_template, request
from app import app
from app.models import Book, PdfBook

ROWS_PER_PAGE = 3


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
