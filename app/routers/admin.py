from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import require_admin
from app.services.admin_service import deactivate_user, remove_book_as_admin


router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/users/{user_id}/deactivate")
def deactivate_user_route(
    user_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_admin),
):
    deactivate_user(db, user_id)
    return RedirectResponse(url="/admin", status_code=303)


@router.post("/books/{book_id}/remove")
def remove_book_route(
    book_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_admin),
):
    remove_book_as_admin(db, book_id)
    return RedirectResponse(url="/admin", status_code=303)
