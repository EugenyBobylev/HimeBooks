from app import db
from app.mupdf import get_cover_fn, get_cover_png_fn, cover_exists, save_cover


class Book(db.Model):
    pdf_name = db.Column(db.String(512), primary_key=True)
    book_name = db.Column(db.String(128))
    cover = None

    def set_cover(self):
        """
        set file name to cover image and if cover image do not exists then create the cover image
        """
        self.cover = get_cover_fn(self.pdf_name)  # file name of cover image without path
        cover_png_fn = get_cover_png_fn(self.cover)  # path and file name of cove image
        exists = cover_exists(cover_png_fn)
        if not exists:
            save_cover(self.pdf_name, cover_png_fn)

    def __repr__(self):
        return f'cover: {self.cover}'


class Catalog(db.Model):
    catalog = db.Column(db.String(512), primary_key=True)

    def __repr__(self):
        return f'{self.catalog}'
