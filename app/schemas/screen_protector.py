from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ScreenProtectorBase(BaseModel):
    device_model: str
    hardness: Optional[str] = None
    price: float

class ScreenProtectorCreate(ScreenProtectorBase):
    pass

class ScreenProtectorUpdate(BaseModel):
    device_model: Optional[str] = None
    hardness: Optional[str] = None
    price: Optional[float] = None

class ScreenProtectorResponse(ScreenProtectorBase):
    id: int
    created_at: datetime
    image_url: str | None = None

    class Config:
        from_attributes = True