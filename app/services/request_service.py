from datetime import date
from sqlalchemy.orm import Session
from app.models import Book, BorrowRequest, Loan, User
from app.errors import ConflictAppError, NotFoundAppError, PermissionAppError, ValidationAppError


def create_borrow_request(db: Session, book_id: int, borrower: User, message: str | None):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundAppError("Book not found")
    if book.owner_id == borrower.id:
        raise ConflictAppError("You cannot request your own book")
    if not book.is_available:
        raise ConflictAppError("Book is not currently available")

    existing = db.query(BorrowRequest).filter(
        BorrowRequest.book_id == book_id,
        BorrowRequest.borrower_id == borrower.id,
        BorrowRequest.status == "pending",
    ).first()
    if existing:
        raise ConflictAppError("You already have a pending request for this book")

    borrow_request = BorrowRequest(
        book_id=book.id,
        borrower_id=borrower.id,
        lender_id=book.owner_id,
        message=message,
        status="pending",
    )
    db.add(borrow_request)
    db.commit()
    db.refresh(borrow_request)
    return borrow_request


def approve_request(db: Session, request_id: int, lender: User, due_date: date):
    req = db.query(BorrowRequest).filter(BorrowRequest.id == request_id).first()
    if not req:
        raise NotFoundAppError("Borrow request not found")
    if req.lender_id != lender.id:
        raise PermissionAppError("You cannot approve this request")
    if req.status != "pending":
        raise ConflictAppError("Only pending requests can be approved")
    if due_date <= date.today():
        raise ValidationAppError("Due date must be in the future")

    book = db.query(Book).filter(Book.id == req.book_id).first()
    if not book or not book.is_available:
        raise ConflictAppError("Book is not available")

    req.status = "approved"
    book.is_available = False

    loan = Loan(
        borrow_request_id=req.id,
        book_id=req.book_id,
        lender_id=req.lender_id,
        borrower_id=req.borrower_id,
        start_date=date.today(),
        due_date=due_date,
        status="active",
    )
    db.add(loan)

    others = db.query(BorrowRequest).filter(
        BorrowRequest.book_id == req.book_id,
        BorrowRequest.id != req.id,
        BorrowRequest.status == "pending",
    ).all()
    for other in others:
        other.status = "rejected"

    db.commit()
    db.refresh(loan)
    return loan


def reject_request(db: Session, request_id: int, lender: User):
    req = db.query(BorrowRequest).filter(BorrowRequest.id == request_id).first()
    if not req:
        raise NotFoundAppError("Borrow request not found")
    if req.lender_id != lender.id:
        raise PermissionAppError("You cannot reject this request")
    if req.status != "pending":
        raise ConflictAppError("Only pending requests can be rejected")
    req.status = "rejected"
    db.commit()
    return req
