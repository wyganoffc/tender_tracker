from app.models import Tender, StatusHistory
from app.schemas import TenderCreate, TenderStatus
from sqlalchemy.orm import Session
import uuid
from fastapi import HTTPException
from app.status_machine import validate_transition
from datetime import datetime


# создание тендера
def create_tender(db: Session, tender_data: TenderCreate) -> Tender:
    """Создать новый тендер со статусом DRAFT"""
    new_tender = Tender(
        title=tender_data.title,
        description=tender_data.description,
        created_by=tender_data.created_by,
        status=TenderStatus.DRAFT  # Всегда начинаем с черновика
    )
    # добавление и сохранение
    db.add(new_tender)
    db.commit()
    db.refresh(new_tender)
    return new_tender


# получение тендера
def get_tender(db: Session, tender_id: uuid.UUID) -> Tender | None:
    """Получить тендер по ID"""
    return db.query(Tender).filter(Tender.id == tender_id).first()


# обновление статуса
def update_tender_status(
        db: Session,
        tender_id: uuid.UUID,
        new_status: TenderStatus,
        changed_by: uuid.UUID,
        reason: str
) -> Tender:
    """Обновить статус тендера с записью в историю"""

    # найти тендер
    tender = get_tender(db, tender_id)
    if not tender:
        raise HTTPException(status_code=404, detail="Tender not found")

    # проверить валидность перехода
    old_status = tender.status
    if not validate_transition(old_status, new_status):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot change from {old_status} to {new_status}"
        )

    # сохранить старый статус в историю
    history = StatusHistory(
        tender_id=tender.id,
        old_status=old_status.value,  # "draft" вместо TenderStatus.DRAFT
        new_status=new_status.value,
        changed_by=changed_by,
        reason=reason
    )
    db.add(history)

    # обновить статус тендера
    tender.status = new_status
    tender.updated_at = datetime.now()

    # сохранить всё в БД
    db.commit()
    db.refresh(tender)

    return tender


# получение истории
def get_tender_history(db: Session, tender_id: uuid.UUID):
    """Получить историю изменений статуса тендера"""
    return (
        db.query(StatusHistory)
        .filter(StatusHistory.tender_id == tender_id)
        .order_by(StatusHistory.created_at.desc())
        .all()
    )
