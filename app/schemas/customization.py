from pydantic import BaseModel
from typing import Optional, Dict
from datetime import datetime

class CustomizationBase(BaseModel):
    device_model: str
    category: str
    image: Optional[str]
    design_params: Optional[Dict]

class CustomizationCreate(CustomizationBase):
    price: float

class CustomizationOut(CustomizationBase):
    id: int
    user_id: int
    price: float
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True