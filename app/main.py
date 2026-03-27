from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app.errors import AppError, app_error_handler
from app.routers import pages, auth, books, requests, loans, admin

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="BookCircle API",
    description="Neighborhood book lending platform",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.add_exception_handler(AppError, app_error_handler)

app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(requests.router)
app.include_router(loans.router)
app.include_router(admin.router)


@app.get("/health")
def health_check():
    return {"status": "ok", "app": "BookCircle"}
