from aiogram import Router, F
from aiogram.types import Message
from services.ai_service import get_ai_response

router = Router()

@router.message(F.text == "Просто выслушай")
async def just_listen(message: Message):
    await message.answer(
        "Я здесь и никуда не тороплюсь\n"
        "Говори — слушаю тебя внимательно"
    )

@router.message(F.text == "Помоги разобраться")
async def help_figure_out(message: Message):
    await message.answer(
        "Хорошо, давай разберёмся вместе\n"
        "Расскажи что происходит?"
    )

@router.message(F.text == "Техники дыхания")
async def breathing(message: Message):
    await message.answer(
        "Давай попробуем вместе\n\n"
        "Дыши со мной:\n\n"
        "Вдох — 4 секунды\n"
        "Задержка — 4 секунды\n"
        "Выдох — 4 секунды\n\n"
        "Повтори 3 раза. Я жду тебя здесь"
    )

@router.message()
async def chat(message: Message):
    user_id = message.from_user.id
    user_text = message.text

    await message.bot.send_chat_action(message.chat.id, "typing")

    try:
        answer = await get_ai_response(user_id, user_text)
        await message.answer(answer)

    except Exception as e:
        await message.answer(
            "Прости, я сейчас немного перегружена\n"
            "Напиши мне через минуту, я обязательно отвечу"
        )