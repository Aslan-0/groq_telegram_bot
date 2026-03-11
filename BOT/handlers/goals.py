from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.db_service import save_goal, get_active_goal, save_goal_progress, get_goal_streak
from keyboards.main_kb import main_menu

router = Router()

class GoalStates(StatesGroup):
    waiting_for_goal = State()

@router.message(Command("цель"))
async def set_goal_command(message: Message, state: FSMContext):
    await message.answer(
        "Отлично! Какую цель ты хочешь поставить?\n\n"
        "Напиши её одним сообщением, например:\n"
        "• Бегать каждое утро\n"
        "• Читать 30 минут в день\n"
        "• Медитировать перед сном"
    )
    await state.set_state(GoalStates.waiting_for_goal)

@router.message(GoalStates.waiting_for_goal)
async def save_user_goal(message: Message, state: FSMContext):
    goal_text = message.text
    user_id = message.from_user.id
    
    goal_id = await save_goal(user_id, goal_text)
    await state.clear()
    
    await message.answer(
        f"Цель установлена!\n\n"
        f"«{goal_text}»\n\n"
        f"Я буду каждый день спрашивать — выполнил ли ты её\n"
        f"Держи курс!",
        reply_markup=main_menu()
    )

@router.message(F.text == "Моя цель")
async def my_goal(message: Message):
    user_id = message.from_user.id
    goal = await get_active_goal(user_id)
    
    if not goal:
        await message.answer(
            "У тебя пока нет активной цели\n\n"
            "Установи её командой /цель",
            reply_markup=main_menu()
        )
        return
    
    streak = await get_goal_streak(user_id, goal['id'])
    
    await message.answer(
        f"Твоя цель:\n"
        f"«{goal['goal_text']}»\n\n"
        f"Выполнено дней подряд: {streak}\n\n"
        f"Выполнил сегодня?",
        reply_markup=goal_progress_keyboard()
    )

@router.message(F.text.in_(["Выполнил", "Не выполнил"]))
async def track_progress(message: Message):
    user_id = message.from_user.id
    goal = await get_active_goal(user_id)
    
    if not goal:
        await message.answer("У тебя нет активной цели", reply_markup=main_menu())
        return
    
    completed = message.text == "Выполнил"
    await save_goal_progress(goal['id'], user_id, completed)
    
    if completed:
        streak = await get_goal_streak(user_id, goal['id'])
        await message.answer(
            f"Отлично!\n\n"
            f"Уже {streak} дней подряд! Так держать",
            reply_markup=main_menu()
        )
    else:
        await message.answer(
            "Ничего страшного! Завтра новый день\n"
            "Главное не сдаваться!",
            reply_markup=main_menu()
        )

def goal_progress_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Выполнил"), KeyboardButton(text="Не выполнил")],
            [KeyboardButton(text="Главное меню")]
        ],
        resize_keyboard=True
    )