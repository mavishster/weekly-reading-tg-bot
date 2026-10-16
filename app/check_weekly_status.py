from app.database.database import get_session
from app.database.repositories import (
    GroupRepository,
    TaskAssignmentRepository,
    WeeklyCycleRepository,
    WeeklyTaskRepository,
)


TELEGRAM_CHAT_ID = -5073655816


def main() -> None:
    with get_session() as session:
        group_repository = GroupRepository(session)
        weekly_cycle_repository = WeeklyCycleRepository(session)
        weekly_task_repository = WeeklyTaskRepository(session)
        task_assignment_repository = TaskAssignmentRepository(
            session
        )

        group = group_repository.get_by_telegram_chat_id(
            telegram_chat_id=TELEGRAM_CHAT_ID,
        )

        if group is None:
            print("Group not found.")
            return

        weekly_cycle = (
            weekly_cycle_repository.get_active_by_group_id(
                group_id=group.id,
            )
        )

        if weekly_cycle is None:
            print("No active weekly cycle found.")
            return

        tasks = (
            weekly_task_repository.get_by_weekly_cycle_id(
                weekly_cycle_id=weekly_cycle.id,
            )
        )

        assignments = (
            task_assignment_repository
            .get_by_weekly_cycle_id(
                weekly_cycle_id=weekly_cycle.id,
            )
        )

        print(
            f"Weekly cycle ID: {weekly_cycle.id}"
        )

        print(
            f"Week start date: "
            f"{weekly_cycle.week_start_date}"
        )

        print(
            f"Completed at: "
            f"{weekly_cycle.completed_at}"
        )

        print(
            f"Total tasks: {len(tasks)}"
        )

        print(
            f"Total assignments: {len(assignments)}"
        )


if __name__ == "__main__":
    main()