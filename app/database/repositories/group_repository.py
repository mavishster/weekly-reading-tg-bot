from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.group import Group


class GroupRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_telegram_chat_id(
        self,
        telegram_chat_id: int,
    ) -> Group | None:
        statement = select(Group).where(
            Group.telegram_chat_id == telegram_chat_id,
        )

        return self.session.scalar(statement)

    def create(
        self,
        telegram_chat_id: int,
        title: str,
    ) -> Group:
        group = Group(
            telegram_chat_id=telegram_chat_id,
            title=title,
        )

        self.session.add(group)
        self.session.flush()

        return group