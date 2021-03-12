from pathlib import Path
import fitz


def get_cover_png(pdf_fn):
    pdf = fitz.open(pdf_fn)
    page = pdf[0]
    pix = page.get_pixmap()
    img_data = pix.getImageData()
    return img_data


def save_png(img_data, png_fn):
    with open(png_fn, 'wb') as f:
        f.write(img_data)


def save_cover_png(pdf_fn, png_fn):
    img_data = get_cover_png(pdf_fn)
    save_png(img_data, png_fn)


def save_all_covers(catalog):
    """Save covers of all pdf books as png"""
    for book_path in catalog.glob('*.pdf'):
        is_exist = Path(book_path).exists()
        if is_exist:
            book_fn = str(book_path)
            img_fn = book_path.stem + '.png'
            save_cover_png(book_fn, img_fn)


if __name__ == '__main__':
    pdf_home = Path.home() / 'Downloads' / 'Books'
    save_all_covers(pdf_home)
