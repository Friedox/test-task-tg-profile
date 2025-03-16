from fastapi import APIRouter, HTTPException
from app.schemas.user import UserOut, UserBase
from app.utils import calculate_countdown
from app.db_helper import get_user_by_id, create_user, get_user_by_telegram_id

router = APIRouter()


@router.get("/users/telegram/{telegram_id}", response_model=UserOut, summary="Get user by Telegram ID")
async def get_user_by_telegram(telegram_id: int):
    user = await get_user_by_telegram_id(telegram_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    countdown = calculate_countdown(user.birthday) if user.birthday else "Birthday not set"
    return UserOut(
        telegram_id=user.telegram_id,
        first_name=user.first_name,
        last_name=user.last_name,
        username=user.username,
        photo_url=user.photo_url,
        birthday=user.birthday,
        countdown=countdown
    )


@router.post("/users/", response_model=dict, summary="Create a new user")
async def create_user_api(data: UserBase):
    existing_user = await get_user_by_telegram_id(data.telegram_id)
    if existing_user:
        return {"id": existing_user.id}

    user = await create_user(**data.dict())
    return {"id": user.id}
