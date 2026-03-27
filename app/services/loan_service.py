from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models import Loan, Book, User
from app.errors import NotFoundAppError, PermissionAppError, ConflictAppError


def list_loans_for_user(db: Session, user: User):
    return db.query(Loan).filter(or_(Loan.borrower_id == user.id, Loan.lender_id == user.id)).all()


def mark_returned(db: Session, loan_id: int, user: User):
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise NotFoundAppError("Loan not found")
    if loan.borrower_id != user.id and loan.lender_id != user.id:
        raise PermissionAppError("You cannot update this loan")
    if loan.status == "completed":
        raise ConflictAppError("Loan is already completed")

    loan.status = "completed"
    loan.returned_at = datetime.utcnow()

    book = db.query(Book).filter(Book.id == loan.book_id).first()
    if book:
        book.is_available = True

    db.commit()
    db.refresh(loan)
    return loan
