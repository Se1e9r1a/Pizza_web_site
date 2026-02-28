from fastapi import APIRouter, Depends, HTTPException
from app.models.case import Case
from app.schemas.case import CaseCreate, CaseUpdate, CaseResponse
from app.core.database import get_db
from typing import List
from sqlalchemy.orm import Session
from app.utils.auth import get_current_user
from app.models.user import User
from app.utils.permissions import get_admin_user

from fastapi import UploadFile, File
from app.utils.file_handler import save_image

router = APIRouter(
    prefix="/cases",
    tags=["Cases"]
)

@router.get("/", response_model=List[CaseResponse])
def get_cases(
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)):
    return db.query(Case).all()

@router.post("/", response_model=CaseResponse)
def create_case(
    case_data: CaseCreate,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)):




    new_case = Case(**case_data.model_dump())

    db.add(new_case)
    db.commit()
    db.refresh(new_case)

    return new_case

@router.get("/{case_id}", response_model=CaseResponse)
def get_case(
    case_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@router.put("/{case_id}", response_model=CaseResponse)
def update_case(
    case_id: int,
    case_data: CaseUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):

    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    if case_data.device_id is not None:
        case.device_id = case_data.device_id
    if case_data.material is not None:
        case.material = case_data.material
    if case_data.color is not None:
        case.color = case_data.color
    if case_data.price is not None:
        case.price = case_data.price
    if case_data.quantity is not None:
        case.quantity = case_data.quantity
    if case_data.is_available is not None:
        case.is_available = case_data.is_available
    db.commit()
    db.refresh(case)
    return case

@router.delete("/{case_id}")
def delete_case(
    case_id: int,
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)):

    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    db.delete(case)
    db.commit()
    return {"message": "Case deleted"}

@router.post("/{case_id}/image", response_model=CaseResponse)
def upload_case_image(
    case_id: int,
    file: UploadFile = File(...),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    case = db.query(Case).filter(Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    image_url = save_image(file, folder="cases")

    case.image_url = image_url
    db.commit()
    db.refresh(case)

    return case