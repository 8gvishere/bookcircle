from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User, Book, BorrowRequest, Loan


templates = Jinja2Templates(directory="app/templates")
router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).order_by(Book.created_at.desc()).limit(6).all()
    return templates.TemplateResponse("index.html", {"request": request, "books": books})


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    my_books = db.query(Book).filter(Book.owner_id == current_user.id).all()
    incoming = db.query(BorrowRequest).filter(BorrowRequest.lender_id == current_user.id).all()
    outgoing = db.query(BorrowRequest).filter(BorrowRequest.borrower_id == current_user.id).all()
    loans = db.query(Loan).filter(or_(Loan.borrower_id == current_user.id, Loan.lender_id == current_user.id)).all()
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": current_user,
            "my_books": my_books,
            "incoming": incoming,
            "outgoing": outgoing,
            "loans": loans,
        },
    )


@router.get("/books", response_class=HTMLResponse)
def books_page(request: Request, db: Session = Depends(get_db)):
    books = db.query(Book).order_by(Book.created_at.desc()).all()
    return templates.TemplateResponse("books.html", {"request": request, "books": books})


@router.get("/books/add", response_class=HTMLResponse)
def add_book_page(request: Request, _: User = Depends(get_current_user)):
    return templates.TemplateResponse("add_book.html", {"request": request})


@router.get("/requests", response_class=HTMLResponse)
def requests_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    incoming = (
        db.query(BorrowRequest)
        .filter(BorrowRequest.lender_id == current_user.id)
        .order_by(BorrowRequest.created_at.desc())
        .all()
    )
    outgoing = (
        db.query(BorrowRequest)
        .filter(BorrowRequest.borrower_id == current_user.id)
        .order_by(BorrowRequest.created_at.desc())
        .all()
    )
    return templates.TemplateResponse("requests.html", {"request": request, "incoming": incoming, "outgoing": outgoing, "user": current_user})


@router.get("/loans", response_class=HTMLResponse)
def loans_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    loans = db.query(Loan).filter(or_(Loan.borrower_id == current_user.id, Loan.lender_id == current_user.id)).all()
    return templates.TemplateResponse("loans.html", {"request": request, "loans": loans, "user": current_user})


@router.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        return RedirectResponse(url="/dashboard", status_code=303)
    users = db.query(User).all()
    books = db.query(Book).all()
    return templates.TemplateResponse("admin.html", {"request": request, "users": users, "books": books, "user": current_user})
