from flask import render_template, request
from app import app
from app.models import Book, PdfBook

ROWS_PER_PAGE = 5


@app.route('/')
@app.route('/index')
def index():
    page = request.args.get('page', 1, type=int)
    db_books = Book.query.paginate(page=page, per_page=ROWS_PER_PAGE).items
    # db_books = Book.query.all()
    books = [PdfBook(book) for book in db_books]
    return render_template('index.html', books=books)
