from sqlalchemy import Column, Integer, String,Float,  DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Sticker(Base):
    __tablename__ = "stickers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    design_type = Column(String(100))  # ← исправлено
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

    case_id = Column(Integer, ForeignKey("cases.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    image_url = Column(String(200), nullable=True)

    case = relationship("Case", back_populates="stickers")