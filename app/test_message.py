from datetime import date

from app.keyboards.weekly import build_weekly_keyboard
from app.templates.weekly_message import build_weekly_message


names = [
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


message = build_weekly_message(
    week_start_date=date.today(),
    names=names,
)

keyboard = build_weekly_keyboard()

print(message)
print("\nCHECKLIST BUTTONS:\n")

for row in keyboard.inline_keyboard:
    for button in row:
        print(button.text, "->", button.callback_data)