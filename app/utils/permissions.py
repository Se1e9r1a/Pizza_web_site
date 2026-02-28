from fastapi import Depends, HTTPException, status
from app.utils.auth import get_current_user
from app.models.user import User

def get_admin_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user