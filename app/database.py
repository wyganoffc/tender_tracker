from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

# создание ссылки и сессии
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


# возвращение сессии
def get_db():
    """Возвращает сессию"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()