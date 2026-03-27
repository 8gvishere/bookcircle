from datetime import datetime, date
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="member", nullable=False)
    is_active = Column(Boolean, default=True)
    neighborhood = Column(String(120), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    books = relationship("Book", back_populates="owner", cascade="all, delete-orphan")
    borrow_requests = relationship("BorrowRequest", foreign_keys="BorrowRequest.borrower_id", back_populates="borrower")
    lending_requests = relationship("BorrowRequest", foreign_keys="BorrowRequest.lender_id", back_populates="lender")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    author = Column(String(120), nullable=False)
    genre = Column(String(80), nullable=False)
    description = Column(Text, nullable=True)
    condition = Column(String(50), default="Good")
    is_available = Column(Boolean, default=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="books")
    requests = relationship("BorrowRequest", back_populates="book", cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="book", cascade="all, delete-orphan")


class BorrowRequest(Base):
    __tablename__ = "borrow_requests"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    lender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    message = Column(Text, nullable=True)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)

    book = relationship("Book", back_populates="requests")
    borrower = relationship("User", foreign_keys=[borrower_id], back_populates="borrow_requests")
    lender = relationship("User", foreign_keys=[lender_id], back_populates="lending_requests")
    loan = relationship("Loan", back_populates="borrow_request", uselist=False)


class Loan(Base):
    __tablename__ = "loans"

    id = Column(Integer, primary_key=True, index=True)
    borrow_request_id = Column(Integer, ForeignKey("borrow_requests.id"), nullable=False, unique=True)
    book_id = Column(Integer, ForeignKey("books.id"), nullable=False)
    lender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    borrower_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date, default=date.today)
    due_date = Column(Date, nullable=False)
    returned_at = Column(DateTime, nullable=True)
    status = Column(String(30), default="active")

    borrow_request = relationship("BorrowRequest", back_populates="loan")
    book = relationship("Book", back_populates="loans")
