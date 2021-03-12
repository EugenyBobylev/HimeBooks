from app import db


class Book(db.Model):
    pdf_name = db.Column(db.String(512), primary_key=True)
    book_name = db.Column(db.String(128))
