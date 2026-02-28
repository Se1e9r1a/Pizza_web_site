from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    role = Column(String(50), default="user")  # "user" или "admin"
    hashed_password = Column(String(256), nullable=False)

    address = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False)
    avatar = Column(String(100), nullable=True)  # будем хранить путь к файлу