from sqlalchemy.orm import Session
from app.models import Book, User
from app.errors import NotFoundAppError, PermissionAppError


def list_books(db: Session):
    return db.query(Book).order_by(Book.created_at.desc()).all()


def create_book(db: Session, owner: User, title: str, author: str, genre: str, description: str | None, condition: str):
    book = Book(
        title=title,
        author=author,
        genre=genre,
        description=description,
        condition=condition,
        owner_id=owner.id,
        is_available=True,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise NotFoundAppError("Book not found")
    return book


def delete_book(db: Session, book_id: int, user: User):
    book = get_book(db, book_id)
    if book.owner_id != user.id and user.role != "admin":
        raise PermissionAppError("You cannot delete this book")
    db.delete(book)
    db.commit()
