from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class TaskAssignment(Base):
    __tablename__ = "task_assignments"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    weekly_task_id: Mapped[int] = mapped_column(
        ForeignKey("weekly_tasks.id"),
        nullable=False,
        unique=True,
    )

    telegram_user_id: Mapped[int] = mapped_column(
        nullable=False,
    )

    telegram_username: Mapped[str | None] = mapped_column(
        nullable=True,
    )

    telegram_full_name: Mapped[str] = mapped_column(
        nullable=False,
    )

    claimed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )