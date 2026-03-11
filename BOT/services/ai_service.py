import os
from groq import Groq
from dotenv import load_dotenv
from services.db_service import save_message, get_history, get_user
from logger import get_logger

load_dotenv()

log = get_logger(__name__)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def get_ai_response(user_id: int, user_text: str) -> str:
    log.info(f"Пользователь {user_id} написал: {user_text[:50]}")

    try:
        history = await get_history(user_id)
        user = await get_user(user_id)
        user_name = user["name"] if user and user["name"] else "друг"

        history_text = ""
        for row in history:
            role = "Пользователь" if row["role"] == "user" else "Алия"
            history_text += f"{role}: {row['message']}\n"

        messages = [
            {
                "role": "system",
                "content": (
                    f"Ты тёплый и заботливый друг по имени Алия. "
                    f"Знай что его зовут {user_name}, но обращайся по имени только иногда, естественно, как живой друг. "
                    "Твоя единственная цель — психологическая поддержка и помощь с эмоциями. "
                    "Если человек просит написать код, решить задачу, перевести текст или что-то не связанное с эмоциями — "
                    "мягко отказывай и возвращай к разговору о чувствах. "
                    "Например: 'Прости, я не умею писать код — я здесь чтобы поддержать тебя эмоционально 💙 Как ты себя чувствуешь?' "
                    "Выслушиваешь человека, поддерживаешь его. "
                    "Отвечаешь коротко, по-русски, без советов если не просят. "
                    "Сначала всегда валидируешь чувства человека. "
                    f"История прошлых разговоров:\n{history_text}"
                    )
            },
            {
                "role": "user",
                "content": user_text
            }
        ]

        await save_message(user_id, "user", user_text)

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )

        answer = response.choices[0].message.content
        await save_message(user_id, "assistant", answer)

        log.info(f"Ответ отправлен пользователю {user_id}")
        return answer

    except Exception as e:
        log.error(f"Ошибка при обработке сообщения от {user_id}: {e}")
        raise e