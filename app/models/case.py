from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    device_id = Column(Integer, ForeignKey("devices.id"), nullable=False)

    material = Column(String(100))
    color = Column(String(55))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    is_available = Column(Boolean, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    image_url = Column(String(200), nullable=True)

    device = relationship("Device", back_populates="cases")
    stickers = relationship("Sticker", back_populates="case")