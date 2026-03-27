from sqlalchemy.orm import Session
from app.models import User
from app.security import hash_password, verify_password, create_access_token
from app.errors import ConflictAppError, AuthAppError


def register_user(db: Session, full_name: str, email: str, password: str, neighborhood: str | None):
    existing = db.query(User).filter(User.email == email.lower()).first()
    if existing:
        raise ConflictAppError("Email already registered")

    user = User(
        full_name=full_name,
        email=email.lower(),
        password_hash=hash_password(password),
        neighborhood=neighborhood,
        role="member",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, email: str, password: str) -> str:
    user = db.query(User).filter(User.email == email.lower()).first()
    if not user or not verify_password(password, user.password_hash):
        raise AuthAppError("Invalid email or password")
    return create_access_token({"sub": str(user.id), "role": user.role})
