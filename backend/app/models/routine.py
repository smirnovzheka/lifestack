from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Routine(Base):
    __tablename__ = "routines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False)   # daily | weekly
    unit: Mapped[str | None] = mapped_column(String(50))             # "pages", "minutes", etc.
    icon: Mapped[str | None] = mapped_column(String(10))             # emoji
    active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    logs: Mapped[list["RoutineLog"]] = relationship("RoutineLog", back_populates="routine", cascade="all, delete-orphan")


class RoutineLog(Base):
    __tablename__ = "routine_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    routine_id: Mapped[int] = mapped_column(Integer, ForeignKey("routines.id"), nullable=False)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    value: Mapped[float | None] = mapped_column(Float)   # e.g. km run, calories
    note: Mapped[str | None] = mapped_column(Text)

    routine: Mapped["Routine"] = relationship("Routine", back_populates="logs")
