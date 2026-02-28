from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), nullable=False)   # Apple, Samsung
    model = Column(String(100), nullable=False)  # iPhone 15
    created_at = Column(DateTime, default=datetime.utcnow)

    image_url = Column(String(200), nullable=True)

    cases = relationship("Case", back_populates="device")
    screen_protectors = relationship("ScreenProtector", back_populates="device")