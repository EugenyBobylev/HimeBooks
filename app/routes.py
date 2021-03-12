from flask import render_template
from app import app
from app.models import Book, PdfBook


@app.route('/')
@app.route('/index')
def index():
    db_books = Book.query.all()
    books = [PdfBook(book) for book in db_books]
    return render_template('index.html', books=books)
