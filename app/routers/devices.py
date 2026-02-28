from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.device import Device
from app.schemas.device import DeviceCreate, DeviceUpdate, DeviceOut
from app.utils.auth import get_current_user
from app.models.user import User
from app.core.database import get_db
from app.utils.permissions import get_admin_user

from fastapi import UploadFile, File
from app.utils.file_handler import save_image

router = APIRouter(
    prefix="/devices",
    tags=["Devices"]
)

@router.post("/", response_model=DeviceOut)
def create_device(
    device: DeviceCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_device = Device(
        brand=device.brand,
        model=device.model
    )

    db.add(new_device)
    db.commit()
    db.refresh(new_device)
    return new_device

@router.get("/", response_model=List[DeviceOut])
def get_devices(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    return db.query(Device).all()

@router.get("/{device_id}", response_model=DeviceOut)
def get_device(
    device_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@router.put("/{device_id}", response_model=DeviceOut)
def update_device(
    device_id: int,
    device_data: DeviceUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    if device_data.brand is not None:
        device.brand = device_data.brand
    if device_data.model is not None:
        device.model = device_data.model
    db.commit()
    db.refresh(device)
    return device

@router.delete("/{device_id}")
def delete_device(
    device_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)):

    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    db.delete(device)
    db.commit()
    return {"message": "Device deleted"}

@router.post("/{device_id}/upload-image", response_model=DeviceOut)
def upload_device_image(
    device_id: int,
    file: UploadFile = File(...),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    image_path = save_image(file, folder="devices")

    device.image_url = image_path
    db.commit()
    db.refresh(device)

    return device