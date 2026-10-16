from sqlalchemy.orm import Session

from app.database.repositories import (
    TaskAssignmentRepository,
    WeeklyCycleRepository,
    WeeklyTaskRepository,
)


class TaskAssignmentService:
    def __init__(self, session: Session) -> None:
        self.session = session

        self.task_assignment_repository = (
            TaskAssignmentRepository(session)
        )

        self.weekly_cycle_repository = (
            WeeklyCycleRepository(session)
        )

        self.weekly_task_repository = WeeklyTaskRepository(
            session
        )

    def toggle_task_assignment(
        self,
        task_id: int,
        telegram_user_id: int,
        telegram_username: str | None,
        telegram_full_name: str,
    ) -> tuple[bool, str, bool]:
        task = self.weekly_task_repository.get_by_id(
            weekly_task_id=task_id,
        )

        if task is None:
            return (
                False,
                "Задача не найдена.",
                False,
            )

        assignment = (
            self.task_assignment_repository
            .get_by_weekly_task_id(
                weekly_task_id=task_id,
            )
        )

        if assignment is not None:
            if assignment.telegram_user_id != telegram_user_id:
                return (
                    False,
                    (
                        f"Эта часть уже отмечена: "
                        f"{assignment.telegram_full_name}"
                    ),
                    False,
                )

            self.task_assignment_repository.delete(
                assignment=assignment,
            )

            self.session.commit()

            return (
                True,
                "Задача снова доступна.",
                False,
            )

        self.task_assignment_repository.create(
            weekly_task_id=task_id,
            telegram_user_id=telegram_user_id,
            telegram_username=telegram_username,
            telegram_full_name=telegram_full_name,
        )

        assignments = (
            self.task_assignment_repository
            .get_by_weekly_cycle_id(
                weekly_cycle_id=task.weekly_cycle_id,
            )
        )

        tasks = (
            self.weekly_task_repository
            .get_by_weekly_cycle_id(
                weekly_cycle_id=task.weekly_cycle_id,
            )
        )

        cycle_completed = (
            len(assignments) == len(tasks)
        )

        if cycle_completed:
            weekly_cycle = (
                self.weekly_cycle_repository.get_by_id(
                    weekly_cycle_id=task.weekly_cycle_id,
                )
            )

            if weekly_cycle is not None:
                self.weekly_cycle_repository.mark_completed(
                    weekly_cycle=weekly_cycle,
                )

        self.session.commit()

        return (
            True,
            f"Задача отмечена: {telegram_full_name}",
            cycle_completed,
        )

    def get_checked_tasks_by_weekly_cycle_id(
        self,
        weekly_cycle_id: int,
    ) -> dict[int, str]:
        assignments = (
            self.task_assignment_repository
            .get_by_weekly_cycle_id(
                weekly_cycle_id=weekly_cycle_id,
            )
        )

        checked_tasks: dict[int, str] = {}

        for assignment in assignments:
            task = self.weekly_task_repository.get_by_id(
                weekly_task_id=assignment.weekly_task_id,
            )

            if task is None:
                continue

            checked_tasks[task.sort_order] = (
                assignment.telegram_full_name
            )

        return checked_tasks