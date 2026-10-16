from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class WeeklyCycle(Base):
    __tablename__ = "weekly_cycles"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    group_id: Mapped[int] = mapped_column(
        ForeignKey("groups.id"),
        nullable=False,
    )

    week_start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    telegram_message_id: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )