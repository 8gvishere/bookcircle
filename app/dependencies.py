from fastapi import Cookie, Depends
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import User
from app.errors import AuthAppError, PermissionAppError


def get_current_user(access_token: str | None = Cookie(default=None), db: Session = Depends(get_db)) -> User:
    if not access_token:
        raise AuthAppError("Please log in first")
    try:
        payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise AuthAppError("Invalid token")
    except JWTError as exc:
        raise AuthAppError("Invalid or expired token") from exc

    user = db.query(User).filter(User.id == int(user_id), User.is_active == True).first()
    if not user:
        raise AuthAppError("User not found or inactive")
    return user


def require_admin(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise PermissionAppError("Admin access required")
    return user
