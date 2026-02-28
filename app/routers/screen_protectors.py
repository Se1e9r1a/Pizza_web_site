from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.screen_protector import ScreenProtector
from app.schemas.screen_protector import (ScreenProtectorCreate, ScreenProtectorUpdate, ScreenProtectorResponse)
from app.utils.auth import get_current_user
from app.models.user import User
from app.core.database import get_db
from app.utils.permissions import get_admin_user

from fastapi import UploadFile, File
from app.utils.file_handler import save_image

router = APIRouter(
    prefix="/screen-protectors",
    tags=["Screen Protectors"]
)

@router.post("/", response_model=ScreenProtectorResponse)
def create_screen_protector(
    protector_data: ScreenProtectorCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    new_protector = ScreenProtector(**protector_data.model_dump())
    db.add(new_protector)
    db.commit()
    db.refresh(new_protector)
    return new_protector

@router.get("/", response_model=List[ScreenProtectorResponse])
def get_screen_protectors(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    return db.query(ScreenProtector).all()

@router.get("/{protector_id}", response_model=ScreenProtectorResponse)
def get_screen_protector(
    protector_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    protector = db.query(ScreenProtector).filter(
        ScreenProtector.id == protector_id
    ).first()
    if not protector:
        raise HTTPException(status_code=404, detail="Screen protector not found")
    return protector

@router.put("/{protector_id}", response_model=ScreenProtectorResponse)
def update_screen_protector(
    protector_id: int,
    protector_data: ScreenProtectorUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    protector = db.query(ScreenProtector).filter(
        ScreenProtector.id == protector_id
    ).first()
    if not protector:
        raise HTTPException(status_code=404, detail="Screen protector not found")
    update_data = protector_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(protector, key, value)
    db.commit()
    db.refresh(protector)
    return protector

@router.delete("/{protector_id}")
def delete_screen_protector(
    protector_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)):

    protector = db.query(ScreenProtector).filter(
        ScreenProtector.id == protector_id
    ).first()

    if not protector:
        raise HTTPException(status_code=404, detail="Screen protector not found")
    db.delete(protector)
    db.commit()
    return {"message": "Screen protector deleted"}

@router.post("/{protector_id}/upload-image", response_model=ScreenProtectorResponse)
def upload_screen_protector_image(
    protector_id: int,
    file: UploadFile = File(...),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    protector = db.query(ScreenProtector).filter(
        ScreenProtector.id == protector_id
    ).first()

    if not protector:
        raise HTTPException(status_code=404, detail="Screen protector not found")

    image_path = save_image(file, folder="screen_protectors")

    protector.image_url = image_path
    db.commit()
    db.refresh(protector)

    return protector