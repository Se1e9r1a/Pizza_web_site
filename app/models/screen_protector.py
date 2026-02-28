from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base
from sqlalchemy.orm import relationship

class ScreenProtector(Base):
    __tablename__ = "screen_protectors"

    id = Column(Integer, primary_key=True, index=True)
    device_model = Column(String(100), nullable=False)
    hardness = Column(String(20))
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    image_url = Column(String(200), nullable=True)

    device_id = Column(Integer, ForeignKey("devices.id"))
    device = relationship("Device", back_populates="screen_protectors")