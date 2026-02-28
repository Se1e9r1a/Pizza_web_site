from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:SavGor@localhost:3306/fastapi_db"

# Создаем движок подключения
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Создаем локальную сессию для каждого запроса
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()