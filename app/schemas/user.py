from app.core.database import Base
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    address: str
    phone: str
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    address: Optional[str]
    phone: Optional[str]
    avatar: Optional[str]

    class Config:
        from_attributes = True