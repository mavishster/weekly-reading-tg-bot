from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.weekly_task import WeeklyTask


class WeeklyTaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(
        self,
        weekly_task_id: int,
    ) -> WeeklyTask | None:
        statement = select(WeeklyTask).where(
            WeeklyTask.id == weekly_task_id,
        )

        return self.session.scalar(statement)

    def get_by_weekly_cycle_id(
        self,
        weekly_cycle_id: int,
    ) -> list[WeeklyTask]:
        statement = (
            select(WeeklyTask)
            .where(
                WeeklyTask.weekly_cycle_id == weekly_cycle_id,
            )
            .order_by(WeeklyTask.sort_order)
        )

        return list(
            self.session.scalars(statement).all()
        )

    def create(
        self,
        weekly_cycle_id: int,
        task_key: str,
        title: str,
        category: str,
        sort_order: int,
    ) -> WeeklyTask:
        weekly_task = WeeklyTask(
            weekly_cycle_id=weekly_cycle_id,
            task_key=task_key,
            title=title,
            category=category,
            sort_order=sort_order,
        )

        self.session.add(weekly_task)
        self.session.flush()

        return weekly_task