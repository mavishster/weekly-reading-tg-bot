from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.weekly_cycle import WeeklyCycle


class WeeklyCycleRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(
        self,
        weekly_cycle_id: int,
    ) -> WeeklyCycle | None:
        statement = select(WeeklyCycle).where(
            WeeklyCycle.id == weekly_cycle_id,
        )

        return self.session.scalar(statement)

    def get_active_by_group_id(
        self,
        group_id: int,
    ) -> WeeklyCycle | None:
        statement = (
            select(WeeklyCycle)
            .where(
                WeeklyCycle.group_id == group_id,
                WeeklyCycle.completed_at.is_(None),
            )
            .order_by(WeeklyCycle.id.desc())
        )

        return self.session.scalar(statement)

    def create(
        self,
        group_id: int,
        week_start_date: date,
    ) -> WeeklyCycle:
        weekly_cycle = WeeklyCycle(
            group_id=group_id,
            week_start_date=week_start_date,
        )

        self.session.add(weekly_cycle)
        self.session.flush()

        return weekly_cycle

    def update_telegram_message_id(
        self,
        weekly_cycle: WeeklyCycle,
        telegram_message_id: int,
    ) -> WeeklyCycle:
        weekly_cycle.telegram_message_id = telegram_message_id

        self.session.flush()

        return weekly_cycle

    def mark_completed(
        self,
        weekly_cycle: WeeklyCycle,
    ) -> WeeklyCycle:
        weekly_cycle.completed_at = datetime.now()

        self.session.flush()

        return weekly_cycle