# app/crud.py
from sqlalchemy.orm import Session
from . import models

def create_book(db: Session, title: str, description: str, filename: str, total_pages: int):
    book = models.Book(
        title=title,
        description=description,
        filename=filename,
        total_pages=total_pages
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def list_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()
