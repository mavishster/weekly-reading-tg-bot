import asyncio
import logging
from datetime import date

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, Message

from app.config import get_settings
from app.database.database import get_session
from app.keyboards.weekly import build_weekly_keyboard
from app.services.member_service import MemberService
from app.services.task_assignment_service import TaskAssignmentService
from app.services.weekly_reading_service import WeeklyReadingService
from app.templates.weekly_message import build_weekly_message


settings = get_settings()

bot = Bot(token=settings.bot_token)
dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message) -> None:
    await message.answer(
        "Привет! Бот для еженедельного чтения запущен."
    )


async def is_group_admin(
    message: Message,
) -> bool:
    if message.chat.type == "private":
        await message.answer(
            "Эта команда доступна только в Telegram-группе."
        )
        return False

    administrators = await bot.get_chat_administrators(
        chat_id=message.chat.id,
    )

    administrator_ids = {
        administrator.user.id
        for administrator in administrators
    }

    if message.from_user is None:
        return False

    if message.from_user.id not in administrator_ids:
        await message.answer(
            "Эта команда доступна только администраторам."
        )
        return False

    return True


@dp.message(Command("members"))
async def members_handler(message: Message) -> None:
    if not await is_group_admin(message):
        return

    with get_session() as session:
        member_service = MemberService(session)

        members = member_service.get_active_members(
            telegram_chat_id=message.chat.id,
        )

    if not members:
        await message.answer(
            "В базе данных нет активных участников группы."
        )
        return

    lines = [
        "👥 Участники группы:",
        "",
    ]

    for index, member in enumerate(members, start=1):
        lines.append(
            f"{index}. {member.id}. {member.name} "
        )

    await message.answer(
        "\n".join(lines)
    )

@dp.message(Command("add"))
async def add_member_handler(message: Message) -> None:
    if not await is_group_admin(message):
        return

    if message.text is None:
        await message.answer(
            "Укажите имя участника.\n\n"
            "Пример:\n"
            "/add Айгуль Талгатовна"
        )
        return

    command_parts = message.text.split(
        maxsplit=1
    )

    if len(command_parts) < 2:
        await message.answer(
            "Укажите имя участника.\n\n"
            "Пример:\n"
            "/add Айгуль Талгатовна"
        )
        return

    name = command_parts[1].strip()

    if not name:
        await message.answer(
            "Укажите имя участника.\n\n"
            "Пример:\n"
            "/add Айгуль Талгатовна"
        )
        return

    with get_session() as session:
        member_service = MemberService(session)

        try:
            member = member_service.add_member(
                telegram_chat_id=message.chat.id,
                name=name,
            )
        except ValueError as error:
            await message.answer(
                str(error)
            )
            return

    await message.answer(
        f"Участник добавлен:\n"
        f"{member.name}"
    )

@dp.message(Command("admin"))
async def admin_handler(message: Message) -> None:
    if not await is_group_admin(message):
        return

    await message.answer(
        "⚙️ Вы являетесь администратором группы."
    )

@dp.message(Command("weekly"))
async def weekly_handler(message: Message) -> None:
    if not await is_group_admin(message):
        return

    today = date.today()

    with get_session() as session:
        member_service = MemberService(session)

        names = member_service.get_active_member_names(
            telegram_chat_id=message.chat.id,
        )

        if not names:
            await message.answer(
                "В базе данных нет активных участников группы."
            )
            return

        weekly_reading_service = WeeklyReadingService(
            session
        )

        weekly_cycle = (
            weekly_reading_service.get_or_create_weekly_cycle(
                telegram_chat_id=message.chat.id,
                group_title=(
                    message.chat.title
                    or "Weekly Reading Group"
                ),
                week_start_date=today,
            )
        )

        task_assignment_service = TaskAssignmentService(
            session
        )

        checked_tasks = (
            task_assignment_service
            .get_checked_tasks_by_weekly_cycle_id(
                weekly_cycle_id=weekly_cycle.id,
            )
        )

    weekly_message = build_weekly_message(
        week_start_date=today,
        names=names,
    )

    weekly_keyboard = build_weekly_keyboard(
        checked_tasks=checked_tasks,
    )

    await message.answer(
        text=weekly_message,
        reply_markup=weekly_keyboard,
    )

@dp.message(Command("edit"))
async def edit_member_handler(message: Message) -> None:
    if not await is_group_admin(message):
        return

    if message.text is None:
        await message.answer(
            "Укажите ID участника и новое имя.\n\n"
            "Пример:\n"
            "/edit 13 Айгуль Талгатовна"
        )
        return

    command_parts = message.text.split(
        maxsplit=2
    )

    if len(command_parts) < 3:
        await message.answer(
            "Укажите ID участника и новое имя.\n\n"
            "Пример:\n"
            "/edit 13 Айгуль Талгатовна"
        )
        return

    try:
        member_id = int(command_parts[1])
    except ValueError:
        await message.answer(
            "ID участника должен быть числом.\n\n"
            "Пример:\n"
            "/edit 13 Айгуль Талгатовна"
        )
        return

    name = command_parts[2].strip()

    if not name:
        await message.answer(
            "Укажите новое имя участника.\n\n"
            "Пример:\n"
            "/edit 13 Айгуль Талгатовна"
        )
        return

    with get_session() as session:
        member_service = MemberService(session)

        try:
            member_service.update_member(
                telegram_chat_id=message.chat.id,
                member_id=member_id,
                name=name,
            )
        except ValueError as error:
            await message.answer(
                str(error)
            )
            return

    await message.answer(
        f"Участник обновлён:\n"
        f"{name}"
    )

@dp.message(Command("remove"))
async def remove_member_handler(message: Message) -> None:
    if not await is_group_admin(message):
        return

    if message.text is None:
        await message.answer(
            "Укажите ID участника.\n\n"
            "Пример:\n"
            "/remove 13"
        )
        return

    command_parts = message.text.split(
        maxsplit=1
    )

    if len(command_parts) < 2:
        await message.answer(
            "Укажите ID участника.\n\n"
            "Пример:\n"
            "/remove 13"
        )
        return

    try:
        member_id = int(command_parts[1])
    except ValueError:
        await message.answer(
            "ID участника должен быть числом.\n\n"
            "Пример:\n"
            "/remove 13"
        )
        return

    with get_session() as session:
        member_service = MemberService(session)

        try:
            member = member_service.deactivate_member(
                telegram_chat_id=message.chat.id,
                member_id=member_id,
            )
        except ValueError as error:
            await message.answer(
                str(error)
            )
            return

        removed_member_name = member.name

    await message.answer(
        f"Участник удалён из активного списка:\n"
        f"{removed_member_name}"
    )

@dp.message(Command("restore"))
async def restore_member_handler(message: Message) -> None:
    if not await is_group_admin(message):
        return

    if message.text is None:
        await message.answer(
            "Укажите ID участника.\n\n"
            "Пример:\n"
            "/restore 13"
        )
        return

    command_parts = message.text.split(
        maxsplit=1
    )

    if len(command_parts) < 2:
        await message.answer(
            "Укажите ID участника.\n\n"
            "Пример:\n"
            "/restore 13"
        )
        return

    try:
        member_id = int(command_parts[1])
    except ValueError:
        await message.answer(
            "ID участника должен быть числом.\n\n"
            "Пример:\n"
            "/restore 13"
        )
        return

    with get_session() as session:
        member_service = MemberService(session)

        try:
            member = member_service.activate_member(
                telegram_chat_id=message.chat.id,
                member_id=member_id,
            )
        except ValueError as error:
            await message.answer(
                str(error)
            )
            return

        restored_member_name = member.name

    await message.answer(
        f"Участник восстановлен:\n"
        f"{restored_member_name}"
    )

@dp.message(Command("inactive"))
async def inactive_members_handler(
    message: Message,
) -> None:
    if not await is_group_admin(message):
        return

    with get_session() as session:
        member_service = MemberService(session)

        members = member_service.get_inactive_members(
            telegram_chat_id=message.chat.id,
        )

    if not members:
        await message.answer(
            "Нет неактивных участников группы."
        )
        return

    lines = [
        "🗃 Неактивные участники:",
        "",
    ]

    for member in members:
        lines.append(
            f"{member.id}. {member.name}"
        )

    await message.answer(
        "\n".join(lines)
    )


@dp.callback_query()
async def checklist_callback_handler(
    callback: CallbackQuery,
) -> None:
    if callback.data is None:
        await callback.answer()
        return

    if not callback.data.startswith("check:"):
        await callback.answer()
        return

    if callback.message is None:
        await callback.answer()
        return

    if callback.message.chat is None:
        await callback.answer()
        return

    task_id = int(callback.data.split(":")[1])
    user = callback.from_user

    with get_session() as session:
        task_assignment_service = TaskAssignmentService(
            session
        )

        task = (
            task_assignment_service
            .weekly_task_repository
            .get_by_id(
                weekly_task_id=task_id,
            )
        )

        if task is None:
            await callback.answer(
                "Задача не найдена.",
                show_alert=True,
            )
            return

        success, response_message, cycle_completed = (
            task_assignment_service.toggle_task_assignment(
                task_id=task_id,
                telegram_user_id=user.id,
                telegram_username=user.username,
                telegram_full_name=user.full_name,
            )
        )

        if not success:
            await callback.answer(
                response_message,
                show_alert=True,
            )
            return

        checked_tasks = (
            task_assignment_service
            .get_checked_tasks_by_weekly_cycle_id(
                weekly_cycle_id=task.weekly_cycle_id,
            )
        )

    keyboard = build_weekly_keyboard(
        checked_tasks=checked_tasks,
    )

    await callback.message.edit_reply_markup(
        reply_markup=keyboard
    )

    await callback.answer(
        response_message
    )

    if cycle_completed:
        await callback.message.answer(
            "Все части на эту неделю выполнены! "
            "Альхамдулиллях."
        )


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s - "
            "%(name)s - "
            "%(levelname)s - "
            "%(message)s"
        ),
    )

    print("Weekly Reading Telegram Bot is starting...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())