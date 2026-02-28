from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base


class PhoneCustomization(Base):
    __tablename__ = "customizations"

    id = Column(Integer, primary_key=True, index=True)

    # --- Пользователь ---
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # --- Выбранные элементы ---
    case_id = Column(Integer, ForeignKey("cases.id"), nullable=True)
    sticker_id = Column(Integer, ForeignKey("stickers.id"), nullable=True)
    screen_protector_id = Column(Integer, ForeignKey("screen_protectors.id"), nullable=True)

    # --- Итоговая информация ---
    total_price = Column(Float, nullable=False)
    status = Column(String(50), default="new")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # --- Relationships ---
    user = relationship("User", backref="customizations")
    case = relationship("Case")
    sticker = relationship("Sticker")
    screen_protector = relationship("ScreenProtector")