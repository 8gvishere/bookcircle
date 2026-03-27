from sqlalchemy.orm import Session
from app.models import User, Book
from app.errors import NotFoundAppError


def list_users(db: Session):
    return db.query(User).order_by(User.created_at.desc()).all()


def deactivate_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise NotFoundAppError("User not found")
    user.is_active = False
    db.commit()
    return user


def remove_book_as_admin(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundAppError("Book not found")
    db.delete(book)
    db.commit()
