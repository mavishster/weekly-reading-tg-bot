from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class WeeklyTask(Base):
    __tablename__ = "weekly_tasks"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    weekly_cycle_id: Mapped[int] = mapped_column(
        ForeignKey("weekly_cycles.id"),
        nullable=False,
    )

    task_key: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    sort_order: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )