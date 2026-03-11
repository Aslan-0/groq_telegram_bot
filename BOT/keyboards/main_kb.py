from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Просто выслушай"),
                KeyboardButton(text="Помоги разобраться")
            ],
            [
                KeyboardButton(text="Техники дыхания"),
                KeyboardButton(text="Моё настроение")
            ],
            [
                KeyboardButton(text="Моя цель")
            ]
        ],
        resize_keyboard=True
    )
    return keyboard