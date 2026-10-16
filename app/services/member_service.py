from sqlalchemy.orm import Session

from app.database.models.member import Member
from app.database.repositories import (
    GroupRepository,
    MemberRepository,
)


class MemberService:
    def __init__(self, session: Session) -> None:
        self.session = session

        self.group_repository = GroupRepository(session)
        self.member_repository = MemberRepository(session)

    def get_active_member_names(
        self,
        telegram_chat_id: int,
    ) -> list[str]:
        members = self.get_active_members(
            telegram_chat_id=telegram_chat_id,
        )

        return [
            member.name
            for member in members
        ]

    def get_active_members(
        self,
        telegram_chat_id: int,
    ) -> list[Member]:
        group = self.group_repository.get_by_telegram_chat_id(
            telegram_chat_id=telegram_chat_id,
        )

        if group is None:
            return []

        return self.member_repository.get_active_by_group_id(
            group_id=group.id,
        )

    def get_member(
        self,
        telegram_chat_id: int,
        member_id: int,
    ) -> Member | None:
        group = self.group_repository.get_by_telegram_chat_id(
            telegram_chat_id=telegram_chat_id,
        )

        if group is None:
            return None

        member = self.member_repository.get_by_id(
            member_id=member_id,
        )

        if member is None:
            return None

        if member.group_id != group.id:
            return None

        return member

    def add_member(
        self,
        telegram_chat_id: int,
        name: str,
    ) -> Member:
        group = self.group_repository.get_by_telegram_chat_id(
            telegram_chat_id=telegram_chat_id,
        )

        if group is None:
            raise ValueError(
                "Telegram group is not registered in the database."
            )

        active_members = (
            self.member_repository.get_active_by_group_id(
                group_id=group.id,
            )
        )

        sort_order = len(active_members) + 1

        member = self.member_repository.create(
            group_id=group.id,
            name=name,
            sort_order=sort_order,
        )

        self.session.commit()

        return member

    def update_member(
        self,
        telegram_chat_id: int,
        member_id: int,
        name: str,
    ) -> Member:
        member = self.get_member(
            telegram_chat_id=telegram_chat_id,
            member_id=member_id,
        )

        if member is None:
            raise ValueError(
                "Участник не найден."
            )

        if not member.is_active:
            raise ValueError(
                "Нельзя изменить неактивного участника."
            )

        self.member_repository.update_name(
            member=member,
            name=name,
        )

        self.session.commit()

        return member

    def deactivate_member(
        self,
        telegram_chat_id: int,
        member_id: int,
    ) -> Member:
        member = self.get_member(
            telegram_chat_id=telegram_chat_id,
            member_id=member_id,
        )

        if member is None:
            raise ValueError(
                "Участник не найден."
            )

        if not member.is_active:
            raise ValueError(
                "Участник уже неактивен."
            )

        self.member_repository.deactivate(
            member=member,
        )

        self.session.commit()

        return member

    def activate_member(
            self,
            telegram_chat_id: int,
            member_id: int,
    ) -> Member:
        member = self.get_member(
            telegram_chat_id=telegram_chat_id,
            member_id=member_id,
        )

        if member is None:
            raise ValueError(
                "Участник не найден."
            )

        if member.is_active:
            raise ValueError(
                "Участник уже активен."
            )

        active_members = (
            self.member_repository.get_active_by_group_id(
                group_id=member.group_id,
            )
        )

        member.sort_order = len(active_members) + 1

        self.member_repository.activate(
            member=member,
        )

        self.session.commit()

        return member

    def get_inactive_members(
            self,
            telegram_chat_id: int,
    ) -> list[Member]:
        group = self.group_repository.get_by_telegram_chat_id(
            telegram_chat_id=telegram_chat_id,
        )

        if group is None:
            return []

        return self.member_repository.get_inactive_by_group_id(
            group_id=group.id,
        )