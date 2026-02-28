from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserOut
from app.core.security import hash_password
from fastapi import UploadFile, File, HTTPException
from app.utils.permissions import get_admin_user
from app.utils.file_handler import save_image

router = APIRouter(prefix="/users")

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed,
        address=user.address,
        phone=user.phone,
        avatar=None  # аватар будет загружаться отдельно
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.get("/", response_model=list[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.post("/{user_id}/upload-avatar", response_model=UserOut)
def upload_user_avatar(
    user_id: int,
    file: UploadFile = File(...),
    admin: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    image_path = save_image(file, folder="avatars")

    user.avatar = image_path
    db.commit()
    db.refresh(user)

    return user