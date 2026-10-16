from app.database.database import get_session
from app.database.repositories import GroupRepository, MemberRepository


TELEGRAM_CHAT_ID = -5456659128


def main() -> None:
    with get_session() as session:
        group_repository = GroupRepository(session)
        member_repository = MemberRepository(session)

        group = group_repository.get_by_telegram_chat_id(
            telegram_chat_id=TELEGRAM_CHAT_ID,
        )

        if group is None:
            print("Group was not found.")
            return

        print(f"Group ID: {group.id}")
        print(f"Group title: {group.title}")

        members = member_repository.get_active_by_group_id(
            group_id=group.id,
        )

        print(f"Active members count: {len(members)}")

        for member in members:
            print(
                f"{member.sort_order}. "
                f"{member.name} "
                f"(active={member.is_active})"
            )


if __name__ == "__main__":
    main()