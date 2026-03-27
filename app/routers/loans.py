from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import User
from app.services.loan_service import mark_returned


router = APIRouter(prefix="/loans", tags=["loans"])


@router.post("/{loan_id}/return")
def return_loan_route(
    loan_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    mark_returned(db, loan_id, current_user)
    return RedirectResponse(url="/loans", status_code=303)
