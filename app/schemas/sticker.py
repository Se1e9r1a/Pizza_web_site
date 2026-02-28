from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class StickerBase(BaseModel):
    name: str
    design_type: Optional[str] = None
    price: float
    quantity: int
    case_id: Optional[int] = None

class StickerCreate(StickerBase):
    pass

class StickerUpdate(BaseModel):
    name: Optional[str] = None
    design_type: Optional[str] = None
    price: Optional[float] = None
    quantity: Optional[int] = None
    case_id: Optional[int] = None

class StickerResponse(StickerBase):
    id: int
    created_at: datetime
    image_url: str | None = None

    class Config:
        from_attributes = True