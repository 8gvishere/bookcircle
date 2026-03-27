from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.services.book_service import create_book, delete_book


router = APIRouter(prefix="/books", tags=["books"])


@router.post("/create")
def create_book_route(
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    description: str = Form(default=""),
    condition: str = Form(default="Good"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    create_book(db, current_user, title, author, genre, description or None, condition)
    return RedirectResponse(url="/books", status_code=303)


@router.post("/{book_id}/delete")
def delete_book_route(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_book(db, book_id, current_user)
    return RedirectResponse(url="/books", status_code=303)
