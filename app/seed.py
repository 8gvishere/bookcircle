from app.database import SessionLocal, engine, Base
from app.models import User, Book
from app.security import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if not db.query(User).filter(User.email == "admin@bookcircle.local").first():
    admin = User(
        full_name="Admin User",
        email="admin@bookcircle.local",
        password_hash=hash_password("admin123"),
        role="admin",
        neighborhood="Central",
    )
    member = User(
        full_name="Test Member",
        email="member@bookcircle.local",
        password_hash=hash_password("member123"),
        role="member",
        neighborhood="Central",
    )
    db.add_all([admin, member])
    db.commit()
    db.refresh(member)

    db.add_all([
        Book(
            title="Clean Code",
            author="Robert C. Martin",
            genre="Software",
            description="Practical coding principles.",
            condition="Good",
            owner_id=member.id,
        ),
        Book(
            title="The Hobbit",
            author="J. R. R. Tolkien",
            genre="Fantasy",
            description="A classic adventure.",
            condition="Fair",
            owner_id=member.id,
        ),
    ])
    db.commit()

print("Seed complete.")
db.close()
