from datetime import datetime
from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.services.request_service import create_borrow_request, approve_request, reject_request


router = APIRouter(prefix="/requests", tags=["requests"])


@router.post("/create/{book_id}")
def create_request_route(
    book_id: int,
    message: str = Form(default=""),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    create_borrow_request(db, book_id, current_user, message or None)
    return RedirectResponse(url="/requests", status_code=303)


@router.post("/{request_id}/approve")
def approve_request_route(
    request_id: int,
    due_date: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    parsed_due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
    approve_request(db, request_id, current_user, parsed_due_date)
    return RedirectResponse(url="/requests", status_code=303)


@router.post("/{request_id}/reject")
def reject_request_route(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    reject_request(db, request_id, current_user)
    return RedirectResponse(url="/requests", status_code=303)
