from datetime import datetime
from pydantic import Field, BaseModel
import uuid
from app.models import TenderStatus


# класс создания тендера
class TenderCreate(BaseModel):
    """Создание тендера"""
    title: str = Field(..., min_length=2, max_length=255)
    description: str = Field(..., min_length=2, max_length=255)
    created_by: uuid.UUID


# класс обновления тендера
class TenderUpdate(BaseModel):
    """Обновление тендера"""
    status: TenderStatus = Field(..., description="Новый статус тендера")
    reason: str = Field(..., min_length=2, max_length=255)


# ответы тендера
class TenderResponse(BaseModel):
    """Ответы тендера"""
    id: uuid.UUID
    title: str = Field(..., min_length=2, max_length=255)
    description: str = Field(..., min_length=2, max_length=255)
    status: TenderStatus = Field(..., description="Новый статус тендера")
    created_by: uuid.UUID
    created_at: datetime
    updated_at: datetime

    # конфигурация
    class Config:
        """Конфигурация ответчика"""
        from_attributes = True


# история ответов
class HistoryResponse(BaseModel):
    """История ответов"""
    id: uuid.UUID
    tender_id: uuid.UUID
    old_status: str = Field(..., min_length=2, max_length=255)
    new_status: str = Field(..., min_length=2, max_length=255)
    changed_by: uuid.UUID
    reason: str = Field(..., min_length=2, max_length=255)
    changed_at: datetime

    # конфигурация
    class Config:
        """Конфигурация истории ответов"""
        from_attributes = True