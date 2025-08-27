from datetime import datetime
from pydantic import BaseModel, EmailStr, constr

Username = constr(strip_whitespace=True, min_length=3, max_length=32, pattern=r"^[A-Za-z0-9_]+$")
Password = constr(min_length=8)

class UserCreate(BaseModel):
    username: Username
    password: Password
    email: EmailStr | None = None
    full_name: str | None = None

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr | None
    full_name: str | None
    created_at: datetime

    class Config:
        from_attributes = True

class UserList(BaseModel):
    items: list[UserPublic]
    total: int
