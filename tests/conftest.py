import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import uuid
from datetime import datetime
from app.database import get_db
from app.routers import app
from app.models import Base, Tender, StatusHistory, TenderStatus

# создание ссылок, сессии
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# фикстура: создание и очистка БД перед каждым тестом
@pytest.fixture(scope="function")
def db_session():
    """Создаёт новую сессию БД для каждого теста"""
    # создаём таблицы
    Base.metadata.create_all(bind=engine)
    # создаём сессию
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()  # откатываем изменения после теста
        db.close()
        # очищаем таблицы
        Base.metadata.drop_all(bind=engine)


# фикстура: Dependency Injection для тестов
@pytest.fixture(scope="function")
def client(db_session):
    """Создаёт тестовый клиент FastAPI с подменой БД"""

    # переопределяем зависимость get_db
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    # подменяем зависимость
    app.dependency_overrides[get_db] = override_get_db
    # создаём тестовый клиент
    with TestClient(app) as test_client:
        yield test_client
    # очищаем переопределение
    app.dependency_overrides.clear()


# фикстура: Тестовые данные (пользователь)
@pytest.fixture(scope="function")
def test_user_id():
    """Возвращает ID тестового пользователя"""
    return uuid.uuid4()


# фикстура: Создание тестового тендера
@pytest.fixture(scope="function")
def test_tender(db_session, test_user_id):
    """Создаёт тестовый тендер в БД"""
    tender = Tender(
        id=uuid.uuid4(),
        title="Тестовый тендер",
        description="Описание тестового тендера",
        status=TenderStatus.DRAFT,
        created_by=test_user_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db_session.add(tender)
    db_session.commit()
    db_session.refresh(tender)
    return tender


# фикстура: Создание истории статусов
@pytest.fixture(scope="function")
def test_history(db_session, test_tender, test_user_id):
    """Создаёт запись истории статуса"""
    history = StatusHistory(
        id=uuid.uuid4(),
        tender_id=test_tender.id,
        old_status=TenderStatus.DRAFT.value,
        new_status=TenderStatus.ACTIVE.value,
        changed_by=test_user_id,
        reason="Тестовое изменение",
        created_at=datetime.now()
    )
    db_session.add(history)
    db_session.commit()
    db_session.refresh(history)
    return history