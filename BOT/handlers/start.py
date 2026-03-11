from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_kb import main_menu
from services.db_service import save_user, get_user

router = Router()

class Registration(StatesGroup):
    waiting_for_name = State()

@router.message(Command("start"))
async def start(message: Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    
    if user and user["name"]:
        # Пользователь уже зарегистрирован
        await message.answer(
            f"Привет снова,\n"
            "Как ты сегодня?",
            reply_markup=main_menu()
        )
    else:
        # Новый пользователь — спрашиваем имя
        await message.answer(
            "Привет! 👋 Я Алия — твой личный друг для поддержки 💙\n\n"
            "Как тебя зовут?"
        )
        await state.set_state(Registration.waiting_for_name)

@router.message(Registration.waiting_for_name)
async def get_name(message: Message, state: FSMContext):
    name = message.text
    await save_user(message.from_user.id, name)
    await state.clear()
    
    await message.answer(
        f"Очень приятно, {name}!\n"
        "Я здесь чтобы выслушать тебя и поддержать\n\n"
        "Расскажи как ты сегодня?",
        reply_markup=main_menu()
    )