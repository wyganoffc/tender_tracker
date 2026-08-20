import enum
import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# базовый класс
class Base(DeclarativeBase):
    """Базовый класс от декларативного"""
    pass


# класс статуса тендера
class TenderStatus(str, enum.Enum):
    """Статусы тендера"""
    DRAFT = "draft"
    ACTIVE = "active"
    WON = "won"
    LOST = "lost"
    CANCELLED = "cancelled"


# тендер
class Tender(Base):
    """Таблица тендер"""
    __tablename__ = "tenders"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[TenderStatus] = mapped_column(default=TenderStatus.DRAFT, nullable=False)
    created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(onupdate=datetime.now, default=datetime.now, nullable=False)


# История статусов
class StatusHistory(Base):
    """Таблица истории статусов"""
    __tablename__ = "status_history"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    tender_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),
                                                 ForeignKey("tenders.id", ondelete="CASCADE"),
                                                 nullable=False
                                                 )
    old_status: Mapped[str] = mapped_column(String(255), nullable=False)
    new_status: Mapped[str] = mapped_column(String(255), nullable=False)
    changed_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.now, nullable=False)