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


def save_cover(pdf_fn: str, png_fn: str):
    img_data = get_cover_png(pdf_fn)
    save_png(img_data, png_fn)


def get_cover_fn(pdf_fn: str):
    """
    Get file name of cover image without path
    """
    book_path = Path(pdf_fn)
    img_fn = book_path.stem + '.png'   # image file name without path
    return img_fn


def get_cover_png_fn(cover_png_fn: str):
    """
    Get path and file name of cover image
    """
    img_path = Path(__file__).parent / 'static' / cover_png_fn
    cover_fn = str(img_path)
    return cover_fn


def cover_exists(cover_fn: str) -> bool:
    is_exists: bool = Path(cover_fn).exists()
    return is_exists


# if __name__ == '__main__':
#    book_pdf_fn = '/home/bobylev/Downloads/Books/Docker_на_практике_2020.pdf'
#    save_cover(book_pdf_fn)
