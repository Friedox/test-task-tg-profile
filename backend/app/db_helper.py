from app.models.user import User
from tortoise.exceptions import DoesNotExist

async def get_user_by_id(user_id: int):
    """
    Retrieve a user by their ID.
    """
    try:
        return await User.get(id=user_id)
    except DoesNotExist:
        return None

async def create_user(**kwargs):
    """
    Create a new user with the provided keyword arguments.
    """
    return await User.create(**kwargs)

async def get_user_by_telegram_id(telegram_id: int):
    """
    Retrieve a user by their Telegram ID.
    """
    try:
        return await User.get(telegram_id=telegram_id)
    except DoesNotExist:
        return None