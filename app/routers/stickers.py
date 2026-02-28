from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.sticker import Sticker
from app.models.case import Case
from app.schemas.sticker import StickerCreate, StickerUpdate, StickerResponse
from app.utils.auth import get_current_user
from app.models.user import User
from app.core.database import get_db
from app.utils.permissions import get_admin_user

from fastapi import UploadFile, File
from app.utils.file_handler import save_image

router = APIRouter(
    prefix="/stickers",
    tags=["Stickers"]
)

@router.post("/", response_model=StickerResponse)
def create_sticker(
    sticker_data: StickerCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    if sticker_data.case_id is not None:
        case = db.query(Case).filter(Case.id == sticker_data.case_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
    new_sticker = Sticker(**sticker_data.model_dump())
    db.add(new_sticker)
    db.commit()
    db.refresh(new_sticker)
    return new_sticker

@router.get("/", response_model=List[StickerResponse])
def get_stickers(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    return db.query(Sticker).all()

@router.get("/{sticker_id}", response_model=StickerResponse)
def get_sticker(
    sticker_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    sticker = db.query(Sticker).filter(Sticker.id == sticker_id).first()
    if not sticker:
        raise HTTPException(status_code=404, detail="Sticker not found")
    return sticker

@router.put("/{sticker_id}", response_model=StickerResponse)
def update_sticker(
    sticker_id: int,
    sticker_data: StickerUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    sticker = db.query(Sticker).filter(Sticker.id == sticker_id).first()
    if not sticker:
        raise HTTPException(status_code=404, detail="Sticker not found")
    update_data = sticker_data.model_dump(exclude_unset=True)

    if "case_id" in update_data:
        case = db.query(Case).filter(Case.id == update_data["case_id"]).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
    for key, value in update_data.items():
        setattr(sticker, key, value)
    db.commit()
    db.refresh(sticker)
    return sticker

@router.delete("/{sticker_id}")
def delete_sticker(
    sticker_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):

    sticker = db.query(Sticker).filter(Sticker.id == sticker_id).first()

    if not sticker:
        raise HTTPException(status_code=404, detail="Sticker not found")

    db.delete(sticker)
    db.commit()

    return {"message": "Sticker deleted"}

@router.post("/{sticker_id}/upload-image", response_model=StickerResponse)
def upload_sticker_image(
    sticker_id: int,
    file: UploadFile = File(...),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    sticker = db.query(Sticker).filter(
        Sticker.id == sticker_id
    ).first()

    if not sticker:
        raise HTTPException(status_code=404, detail="Sticker not found")

    # если нужно удалять старую картинку
    import os
    if sticker.image_url:
        old_path = sticker.image_url.replace("/static/", "media/")
        if os.path.exists(old_path):
            os.remove(old_path)

    image_path = save_image(file, folder="stickers")

    sticker.image_url = image_path
    db.commit()
    db.refresh(sticker)

    return sticker