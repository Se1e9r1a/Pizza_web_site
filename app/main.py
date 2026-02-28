from fastapi import FastAPI
from app.routers import users  # подключаем роутер пользователей
from app.routers import customizations # подключаем роутер кастомизации
from app.routers import auth # подключаем роутер авторизации
from app.routers import cases # подключаем роутер чехлов
from app.routers import devices # подключаем роутер устройств
from app.routers import stickers # подключаем роутер стикеров
from app.routers import screen_protectors # подключаем роутер чехлов
from app.core.database import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Создаем все таблицы
os.makedirs("media", exist_ok=True)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Phone Customization Backend")
app.mount("/static", StaticFiles(directory="media"), name="media")

# Подключаем роутеры
app.include_router(users.router)
app.include_router(customizations.router)
app.include_router(auth.router)
app.include_router(cases.router)
app.include_router(devices.router)
app.include_router(stickers.router)
app.include_router(screen_protectors.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000/"],  # фронтенд
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
