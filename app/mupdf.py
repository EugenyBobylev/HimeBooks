from pathlib import Path
import fitz


def get_cover_png(pdf_fn: str):
    pdf = fitz.open(pdf_fn)
    page = pdf[0]
    pix = page.get_pixmap()
    img_data = pix.getImageData()
    return img_data


def save_png(img_data, png_fn: str):
    with open(png_fn, 'wb') as f:
        f.write(img_data)


def save_cover_png(pdf_fn: str, png_fn: str):
    img_data = get_cover_png(pdf_fn)
    save_png(img_data, png_fn)


def save_cover(pdf_fn: str):
    book_path = Path(pdf_fn)
    book_exists = Path(book_path).exists()
    if book_exists:
        img_fn = book_path.stem + '.png'   # image file name without path
        img_path = Path(__file__).parent / 'static' / img_fn
        cover_exists = Path(img_path).exists()
        if not cover_exists:
            img_fn = str(img_path)
            save_cover_png(pdf_fn, img_fn)


# if __name__ == '__main__':
#    book_pdf_fn = '/home/bobylev/Downloads/Books/Docker_на_практике_2020.pdf'
#    save_cover(book_pdf_fn)
