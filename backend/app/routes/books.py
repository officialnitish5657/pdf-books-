from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse, FileResponse
from app.database import get_db
from app.models import Book
import shutil
import os
from datetime import datetime
import fitz  # PyMuPDF

router = APIRouter(prefix="/books", tags=["Books"])

# Absolute folders (safe for Render)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "../uploads")
PAGES_DIR = os.path.join(BASE_DIR, "../static/pages")


# ✅ Upload Book
@router.post("/")
async def upload_book(
    title: str = Form(...),
    description: str = Form(""),
    rating: float = Form(0),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Unique filename (timestamp)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Store DB record
    new_book = Book(
        title=title,
        description=description,
        rating=rating,
        file_path=file_path
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    # Return clean JSON (no ORM)
    return {
        "message": f"Book '{new_book.title}' uploaded successfully",
        "book": {
            "id": new_book.id,
            "title": new_book.title,
            "description": new_book.description,
            "rating": new_book.rating,
            "file_path": new_book.file_path,
        }
    }


# ✅ Get all books
@router.get("/")
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return [
        {
            "id": b.id,
            "title": b.title,
            "description": b.description,
            "rating": b.rating,
            "file_path": b.file_path,
            "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(b, "created_at") else None
        }
        for b in books
    ]

@router.get("/{book_id}/")
def get_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return [
        {
            "id": b.id,
            "title": b.title,
            "description": b.description,
            "rating": b.rating,
            "file_path": b.file_path,
            "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(b, "created_at") else None,
        }
        for b in books
    ]

# ✅ Generate book pages (lazy loaded)
@router.get("/{book_id}/pages")
def get_book_pages(book_id: int, start: int = 0, count: int = 5, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    pdf_path = book.file_path
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF file not found")

    os.makedirs(PAGES_DIR, exist_ok=True)
    doc = fitz.open(pdf_path)
    total_pages = doc.page_count
    end = min(start + count, total_pages)

    image_urls = []
    for page_number in range(start, end):
        page = doc.load_page(page_number)
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
        image_path = os.path.join(PAGES_DIR, f"book{book_id}_page{page_number + 1}.png")
        pix.save(image_path)
        image_urls.append(f"/static/pages/book{book_id}_page{page_number + 1}.png")

    doc.close()

    return JSONResponse({
        "book_id": book_id,
        "start": start,
        "count": len(image_urls),
        "total_pages": total_pages,
        "pages": image_urls
    })


# ✅ Download full PDF
@router.get("/{book_id}/file")
def get_book_pdf(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    pdf_path = book.file_path
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF not found")

    return FileResponse(pdf_path, media_type="application/pdf")

# from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
# from sqlalchemy.orm import Session
# from fastapi.responses import JSONResponse, FileResponse
# from app.database import get_db
# from app.models import Book
# import shutil
# import os
# from datetime import datetime
# import fitz  # PyMuPDF

# router = APIRouter(prefix="/books", tags=["Books"])

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_DIR = os.path.join(BASE_DIR, "../uploads")
# PAGES_DIR = os.path.join(BASE_DIR, "../static/pages")


# # ✅ Upload Book
# @router.post("/")
# async def upload_book(
#     title: str = Form(...),
#     description: str = Form(""),
#     rating: float = Form(0),
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)
# ):
#     os.makedirs(UPLOAD_DIR, exist_ok=True)
#     timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
#     filename = f"{timestamp}_{file.filename}"
#     file_path = os.path.join(UPLOAD_DIR, filename)

#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     new_book = Book(title=title, description=description, rating=rating, file_path=file_path)
#     db.add(new_book)
#     db.commit()
#     db.refresh(new_book)

#     return {
#         "message": f"Book '{new_book.title}' uploaded successfully",
#         "book": {
#             "id": new_book.id,
#             "title": new_book.title,
#             "description": new_book.description,
#             "rating": new_book.rating,
#             "file_path": new_book.file_path,
#         },
#     }


# # ✅ Get all books
# @router.get("/")
# def get_books(db: Session = Depends(get_db)):
#     books = db.query(Book).all()
#     return [
#         {
#             "id": b.id,
#             "title": b.title,
#             "description": b.description,
#             "rating": b.rating,
#             "file_path": b.file_path,
#             "created_at": b.created_at.strftime("%Y-%m-%d %H:%M:%S") if hasattr(b, "created_at") else None,
#         }
#         for b in books
#     ]





# # ✅ Generate book pages (lazy loaded)
# @router.get("/{book_id}/pages")
# def get_book_pages(book_id: int, start: int = 0, count: int = 5, db: Session = Depends(get_db)):
#     book = db.query(Book).filter(Book.id == book_id).first()
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")

#     pdf_path = book.file_path
#     if not os.path.exists(pdf_path):
#         raise HTTPException(status_code=404, detail="PDF file not found")

#     os.makedirs(PAGES_DIR, exist_ok=True)
#     doc = fitz.open(pdf_path)
#     total_pages = doc.page_count
#     end = min(start + count, total_pages)

#     image_urls = []
#     for page_number in range(start, end):
#         page = doc.load_page(page_number)
#         pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
#         image_path = os.path.join(PAGES_DIR, f"book{book_id}_page{page_number + 1}.png")
#         pix.save(image_path)
#         image_urls.append(f"/static/pages/book{book_id}_page{page_number + 1}.png")

#     doc.close()

#     return JSONResponse({
#         "book_id": book_id,
#         "start": start,
#         "count": len(image_urls),
#         "total_pages": total_pages,
#         "pages": image_urls,
#     })


# # ✅ Download full PDF
# @router.get("/{book_id}/file")
# def get_book_pdf(book_id: int, db: Session = Depends(get_db)):
#     book = db.query(Book).filter(Book.id == book_id).first()
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")

#     pdf_path = book.file_path
#     if not os.path.exists(pdf_path):
#         raise HTTPException(status_code=404, detail="PDF not found")

#     return FileResponse(pdf_path, media_type="application/pdf")
