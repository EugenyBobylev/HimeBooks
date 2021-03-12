from flask import render_template
from app import app, db
from app.models import Book


@app.route('/')
@app.route('/index')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)
