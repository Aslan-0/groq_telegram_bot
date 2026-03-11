from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.db_service import connect_db, get_all_users, get_total_users, get_messages_today, get_mood_stats, get_user_conversations
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup():
    await connect_db()

@app.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    users = await get_all_users()
    total_users = await get_total_users()
    messages_today = await get_messages_today()
    mood_stats = await get_mood_stats()
    
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "users": users,
        "total_users": total_users,
        "messages_today": messages_today,
        "mood_stats": mood_stats
    })

@app.get("/user/{user_id}", response_class=HTMLResponse)
async def user_detail(request: Request, user_id: int):
    conversations = await get_user_conversations(user_id)
    
    return templates.TemplateResponse("user_detail.html", {
        "request": request,
        "user_id": user_id,
        "conversations": conversations
    })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)