from fastapi import FastAPI, HTTPException, Depends
from app.schemas import TenderCreate, TenderResponse, TenderUpdate, HistoryResponse
from app.crud import create_tender, get_tender, update_tender_status, get_tender_history
from sqlalchemy.orm import Session
import uuid
from app.database import get_db

# создание приложения
app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "Tender Tracker API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


# обработка пост
@app.post("/tenders", status_code=201)
def tender_post(tc: TenderCreate, db: Session = Depends(get_db)):
    """Оброботчик POST"""
    tender = create_tender(db, tc)
    return TenderResponse.model_validate(tender)


# обработка гет
@app.get("/tenders/{tender_id}", status_code=200)
def tender_get(tender_id: uuid.UUID, db: Session = Depends(get_db)):
    """Обработчик GET"""
    tender = get_tender(db, tender_id)
    if tender is None:
        raise HTTPException(status_code=404, detail="Tender not found")
    return TenderResponse.model_validate(tender)


# обработка патч
@app.patch("/tenders/{tender_id}/status")
def tender_patch(tu: TenderUpdate, tender_id: uuid.UUID, db: Session = Depends(get_db)):
    """Обработчик PATCH"""
    tender = update_tender_status(db, tender_id, tu.status, tu.changed_by, tu.reason)
    return TenderResponse.model_validate(tender)


# обработка гет
@app.get("/tenders/{tender_id}/history", status_code=200)
def tender_history(tender_id: uuid.UUID, db: Session = Depends(get_db)):
    """Обработка GET"""
    existing_tender = get_tender(db, tender_id)
    if existing_tender is None:
        raise HTTPException(status_code=404, detail="Tender not found")
    history = get_tender_history(db, tender_id)
    return [HistoryResponse.model_validate(record) for record in history]
