# app/pdf_processor.py
import fitz  # PyMuPDF
from pathlib import Path
from typing import List

STATIC_DIR = Path(__file__).parent / "static"
PDF_DIR = STATIC_DIR / "pdfs"
IMG_DIR = STATIC_DIR / "images"

PDF_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)

def ensure_book_image_dir(book_id: int) -> Path:
    """Make sure the folder for a specific book's images exists."""
    path = IMG_DIR / str(book_id)
    path.mkdir(parents=True, exist_ok=True)
    return path

def get_total_pages(pdf_path: str) -> int:
    """Get number of pages in a PDF file."""
    doc = fitz.open(pdf_path)
    count = doc.page_count
    doc.close()
    return count

def render_pages_to_images(book_id: int, pdf_path: str, start: int, count: int) -> List[str]:
    """
    Render pages [start, start+count-1] to images.
    Returns list of relative URLs for generated image files.
    """
    start = int(start)
    count = int(count)
    doc = fitz.open(str(pdf_path))
    img_dir = ensure_book_image_dir(book_id)
    urls = []

    for i in range(start, min(start + count, doc.page_count)):
        page_number = i + 1  # 1-indexed file names
        output_path = img_dir / f"{page_number}.jpg"

        # Only generate if image doesn’t already exist
        if not output_path.exists():
            page = doc.load_page(i)
            pix = page.get_pixmap(dpi=150)  # 150 DPI = good balance of quality/size
            pix.save(str(output_path))

        urls.append(f"/static/images/{book_id}/{page_number}.jpg")

    doc.close()
    return urls
