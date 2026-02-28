from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DeviceBase(BaseModel):
    brand: str
    model: str

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None

class DeviceOut(DeviceBase):
    id: int
    created_at: datetime
    image_url: str | None = None

    class Config:
        from_attributes = True