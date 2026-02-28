from typing import List
from app.models.customization import PhoneCustomization
from app.schemas.customization import CustomizationCreate, CustomizationOut
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.auth import get_current_user
from app.models.user import User
from app.core.database import get_db
from app.utils.permissions import get_admin_user

router = APIRouter(
    prefix="/customizations",
    tags=["Customizations"]
)

@router.post("/", response_model=CustomizationOut)
def create_customization(
    customization: CustomizationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_customization = PhoneCustomization(
        user_id=current_user.id,  # ← вот замена
        device_model=customization.device_model,
        category=customization.category,
        image=customization.image,
        design_params=customization.design_params,
        price=customization.price,
        status="new"
    )

    db.add(new_customization)
    db.commit()
    db.refresh(new_customization)

    return new_customization

@router.get("/", response_model=List[CustomizationOut])
def get_customizations(db: Session = Depends(get_db)):
    return db.query(PhoneCustomization).all()

@router.get("/{customization_id}", response_model=CustomizationOut)
def get_customization(customization_id: int, db: Session = Depends(get_db)):
    customization = db.query(PhoneCustomization).filter(
        PhoneCustomization.id == customization_id
    ).first()

    if not customization:
        raise HTTPException(status_code=404, detail="Customization not found")

    return customization

@router.put("/{customization_id}/status")
def update_status(
    customization_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    customization = db.query(PhoneCustomization).filter(
        PhoneCustomization.id == customization_id
    ).first()

    if not customization:
        raise HTTPException(status_code=404, detail="Customization not found")

    customization.status = status
    db.commit()
    db.refresh(customization)

    return {"message": "Status updated"}

@router.delete("/{customization_id}")
def delete_customization(customization_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)):
    customization = db.query(PhoneCustomization).filter(
    PhoneCustomization.id == customization_id
    ).first()

    if not customization:
        raise HTTPException(status_code=404, detail="Customization not found")

    db.delete(customization)
    db.commit()

    return {"message": "Customization deleted"}

# ---- Получаем все кастомизации текущего пользователя. ----
@router.get("/me")
def read_my_customizations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user.customizations  # relationship из модели PhoneCustomization