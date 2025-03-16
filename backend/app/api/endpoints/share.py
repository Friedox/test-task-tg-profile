from fastapi import APIRouter, HTTPException
import requests
from app.config import settings

router = APIRouter()

BOT_TOKEN = settings.telegram_bot_token


@router.post("/share_message/{telegram_id}")
async def create_prepared_message(telegram_id: int):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/savePreparedInlineMessage"

    payload = {
        "user_id": telegram_id,
        "result": {
            "type": "article",
            "id": f"profile-{telegram_id}",
            "title": "Узнай мой день рождения!",
            "input_message_content": {
                "message_text": f"🎉 Узнай мой день рождения! Смотреть 👉 https://t.me/BirthdayProfileBot?startapp={telegram_id}"
            },
            "description": "День рождения и профиль в боте 🎉"
        },
        "allow_user_chats": True,
        "allow_group_chats": True
    }

    response = requests.post(url, json=payload)

    if response.ok:
        result = response.json()
        return {
            "prepared_message_id": result["result"]["id"],
            "expires_at": result["result"]["expiration_date"]
        }
    else:
        raise HTTPException(status_code=500, detail=f"Telegram API error: {response.text}")
