# app/models.py
from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from .database import Base

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    filename = Column(String)          # Stored PDF filename
    total_pages = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    file_path = Column(String)
    rating_count = Column(Integer, default=0)
    cover_image = Column(String, nullable=True)  # Thumbnail path
    created_at = Column(DateTime, default=datetime.utcnow)

# class Book(Base):
#     __tablename__ = "books"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String)
#     filename = Column(String)  # stored pdf file name
#     total_pages = Column(Integer, default=0)
#     rating = Column(Float, default=0.0)
#     created_at = Column(DateTime, default=datetime.utcnow)
