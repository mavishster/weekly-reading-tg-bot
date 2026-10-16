from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models.member import Member


class MemberRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_id(
        self,
        member_id: int,
    ) -> Member | None:
        statement = select(Member).where(
            Member.id == member_id,
        )

        return self.session.scalar(statement)

    def get_active_by_group_id(
        self,
        group_id: int,
    ) -> list[Member]:
        statement = (
            select(Member)
            .where(
                Member.group_id == group_id,
                Member.is_active.is_(True),
            )
            .order_by(Member.sort_order)
        )

        return list(
            self.session.scalars(statement).all()
        )

    def get_all_by_group_id(
        self,
        group_id: int,
    ) -> list[Member]:
        statement = (
            select(Member)
            .where(
                Member.group_id == group_id,
            )
            .order_by(Member.sort_order)
        )

        return list(
            self.session.scalars(statement).all()
        )

    def create(
        self,
        group_id: int,
        name: str,
        sort_order: int,
    ) -> Member:
        member = Member(
            group_id=group_id,
            name=name,
            sort_order=sort_order,
            is_active=True,
        )

        self.session.add(member)
        self.session.flush()

        return member

    def update_name(
        self,
        member: Member,
        name: str,
    ) -> Member:
        member.name = name

        self.session.flush()

        return member

    def deactivate(
        self,
        member: Member,
    ) -> Member:
        member.is_active = False

        self.session.flush()

        return member

    def activate(
            self,
            member: Member,
    ) -> Member:
        member.is_active = True

        self.session.flush()

        return member

    def get_inactive_by_group_id(
            self,
            group_id: int,
    ) -> list[Member]:
        statement = (
            select(Member)
            .where(
                Member.group_id == group_id,
                Member.is_active.is_(False),
            )
            .order_by(Member.sort_order)
        )

        return list(
            self.session.scalars(statement).all()
        )