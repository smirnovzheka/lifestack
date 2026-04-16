from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class WeeklyGoal(Base):
    __tablename__ = "weekly_goals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    week_start: Mapped[date] = mapped_column(Date, nullable=False)   # always Monday
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    project_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("projects.id"), nullable=True)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    project: Mapped["Project | None"] = relationship("Project", back_populates="weekly_goals")
