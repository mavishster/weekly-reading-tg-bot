from app.database.database import get_session
from app.database.repositories import GroupRepository
from app.services.member_service import MemberService


TELEGRAM_CHAT_ID = -5073655816

GROUP_TITLE = "Weekly Reading Group"

MEMBER_NAMES = [
    "Анель",
    "Баршын",
    "Альбина Серикбай",
    "Эльмира Болтекова",
    "Сая Жапарова",
    "Ляззат",
    "Айнур",
    "Ақерке",
    "Юлия",
]


def main() -> None:
    with get_session() as session:
        group_repository = GroupRepository(session)

        group = group_repository.get_by_telegram_chat_id(
            telegram_chat_id=TELEGRAM_CHAT_ID,
        )

        if group is None:
            group = group_repository.create(
                telegram_chat_id=TELEGRAM_CHAT_ID,
                title=GROUP_TITLE,
            )

            session.commit()

        member_service = MemberService(session)

        existing_members = member_service.get_active_member_names(
            telegram_chat_id=TELEGRAM_CHAT_ID,
        )

        for name in MEMBER_NAMES:
            if name not in existing_members:
                member_service.add_member(
                    telegram_chat_id=TELEGRAM_CHAT_ID,
                    name=name,
                )

    print("Group and members seeded successfully.")


if __name__ == "__main__":
    main()