from fastapi import APIRouter, Depends, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.auth_service import register_user, login_user


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    neighborhood: str = Form(default=""),
    db: Session = Depends(get_db),
):
    register_user(db, full_name, email, password, neighborhood or None)
    return RedirectResponse(url="/login", status_code=303)


@router.post("/login")
def login(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    token = login_user(db, email, password)
    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie("access_token", token, httponly=True, samesite="lax")
    return response


@router.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response
