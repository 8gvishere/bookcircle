from datetime import date
from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    full_name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)
    neighborhood: str | None = Field(default=None, max_length=120)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    author: str = Field(min_length=1, max_length=120)
    genre: str = Field(min_length=1, max_length=80)
    description: str | None = Field(default=None, max_length=1000)
    condition: str = Field(default="Good", max_length=50)


class RequestCreate(BaseModel):
    message: str | None = Field(default=None, max_length=500)


class LoanApprove(BaseModel):
    due_date: date
