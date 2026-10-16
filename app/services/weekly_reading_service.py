from datetime import date

from sqlalchemy.orm import Session

from app.data.checklist import CHECKLIST_ITEMS
from app.database.repositories import (
    GroupRepository,
    WeeklyCycleRepository,
    WeeklyTaskRepository,
)


class WeeklyReadingService:
    def __init__(self, session: Session) -> None:
        self.session = session

        self.group_repository = GroupRepository(session)
        self.weekly_cycle_repository = WeeklyCycleRepository(session)
        self.weekly_task_repository = WeeklyTaskRepository(session)

    def get_or_create_weekly_cycle(
        self,
        telegram_chat_id: int,
        group_title: str,
        week_start_date: date,
    ):
        group = self.group_repository.get_by_telegram_chat_id(
            telegram_chat_id=telegram_chat_id,
        )

        if group is None:
            group = self.group_repository.create(
                telegram_chat_id=telegram_chat_id,
                title=group_title,
            )

        weekly_cycle = (
            self.weekly_cycle_repository.get_active_by_group_id(
                group_id=group.id,
            )
        )

        if weekly_cycle is None:
            weekly_cycle = self.weekly_cycle_repository.create(
                group_id=group.id,
                week_start_date=week_start_date,
            )

            for item in CHECKLIST_ITEMS:
                self.weekly_task_repository.create(
                    weekly_cycle_id=weekly_cycle.id,
                    task_key=f"{item['category']}_{item['sort_order']}",
                    title=item["title"],
                    category=item["category"],
                    sort_order=item["sort_order"],
                )

        self.session.commit()

        return weekly_cycle