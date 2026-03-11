from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_kb import main_menu
from services.db_service import save_mood

router = Router()

@router.message(F.text == "Моё настроение")
async def ask_mood(message: Message):
    await message.answer(
        "Как ты себя чувствуешь сейчас?\n\n"
        "Нажми на одну из кнопок ниже",
        reply_markup=mood_keyboard()
    )

def mood_keyboard():
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Хорошо"), KeyboardButton(text="Нормально")],
            [KeyboardButton(text="Грустно"), KeyboardButton(text="Тревожно")],
            [KeyboardButton(text="Раздражён")],
            [KeyboardButton(text="Главное меню")]
        ],
        resize_keyboard=True
    )

@router.message(F.text.in_(["Хорошо", "Нормально", "Грустно", "Тревожно", "Раздражён"]))
async def save_mood_handler(message: Message):
    await save_mood(
        user_id=message.from_user.id,
        mood=message.text
    )
    
    await message.answer(
        f"Записал — {message.text}\n\n"
        "Спасибо что поделился \n"
        "Хочешь поговорить об этом?",
        reply_markup=main_menu()
    )

@router.message(F.text == "🏠 Главное меню")
async def main_menu_handler(message: Message):
    await message.answer("Главное меню 🏠", reply_markup=main_menu())