from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.data.checklist import CHECKLIST_ITEMS


def build_weekly_keyboard(
    checked_tasks: dict[int, str] | None = None,
) -> InlineKeyboardMarkup:
    checked_tasks = checked_tasks or {}

    keyboard = [
        [
            InlineKeyboardButton(
                text="Cevsen",
                callback_data="section:cevsen",
            )
        ]
    ]

    for item in CHECKLIST_ITEMS:
        if item["category"] == "dua":
            task_id = item["sort_order"]

            if task_id in checked_tasks:
                button_text = (
                    f"✅ {item['title']} — "
                    f"{checked_tasks[task_id]}"
                )
            else:
                button_text = f"☐ {item['title']}"

            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=button_text,
                        callback_data=f"check:{task_id}",
                    )
                ]
            )

    keyboard.append(
        [
            InlineKeyboardButton(
                text="Sakine",
                callback_data="section:sakine",
            )
        ]
    )

    for item in CHECKLIST_ITEMS:
        if item["category"] == "sakine":
            task_id = item["sort_order"]

            if task_id in checked_tasks:
                button_text = (
                    f"✅ {item['title']} — "
                    f"{checked_tasks[task_id]}"
                )
            else:
                button_text = f"☐ {item['title']}"

            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=button_text,
                        callback_data=f"check:{task_id}",
                    )
                ]
            )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )