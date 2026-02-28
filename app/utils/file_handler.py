import os
import shutil
from uuid import uuid4
from fastapi import UploadFile, HTTPException


def save_image(file: UploadFile, folder: str, old_path: str | None = None) -> str:
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    os.makedirs(folder, exist_ok=True)

    extension = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{extension}"
    file_path = os.path.join(folder, filename)

    # Удаляем старый файл
    if old_path:
        old_file = old_path.lstrip("/")
        if os.path.exists(old_file):
            os.remove(old_file)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/{file_path}"