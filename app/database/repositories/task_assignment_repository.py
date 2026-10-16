from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.task_assignment import TaskAssignment
from app.database.models.weekly_task import WeeklyTask


class TaskAssignmentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_weekly_task_id(
        self,
        weekly_task_id: int,
    ) -> TaskAssignment | None:
        statement = select(TaskAssignment).where(
            TaskAssignment.weekly_task_id == weekly_task_id,
        )

        return self.session.scalar(statement)

    def get_by_weekly_cycle_id(
        self,
        weekly_cycle_id: int,
    ) -> list[TaskAssignment]:
        statement = (
            select(TaskAssignment)
            .join(
                WeeklyTask,
                TaskAssignment.weekly_task_id
                == WeeklyTask.id,
            )
            .where(
                WeeklyTask.weekly_cycle_id
                == weekly_cycle_id,
            )
        )

        return list(
            self.session.scalars(statement).all()
        )

    def create(
        self,
        weekly_task_id: int,
        telegram_user_id: int,
        telegram_username: str | None,
        telegram_full_name: str,
    ) -> TaskAssignment:
        assignment = TaskAssignment(
            weekly_task_id=weekly_task_id,
            telegram_user_id=telegram_user_id,
            telegram_username=telegram_username,
            telegram_full_name=telegram_full_name,
        )

        self.session.add(assignment)
        self.session.flush()

        return assignment

    def delete(
        self,
        assignment: TaskAssignment,
    ) -> None:
        self.session.delete(assignment)
        self.session.flush()