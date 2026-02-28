from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CaseBase(BaseModel):
    device_id: int
    material: Optional[str] = None
    color: Optional[str] = None
    price: float
    quantity: int
    is_available: bool

class CaseCreate(CaseBase):
    pass

class CaseUpdate(BaseModel):
    material: Optional[str] = None
    color: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    is_available: Optional[bool] = None

class CaseResponse(CaseBase):
    id: int
    created_at: datetime
    image_url: str | None = None

    class Config:
        from_attributes = True