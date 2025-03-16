from pydantic import BaseModel
from datetime import date

class UserBase(BaseModel):
    telegram_id: int
    first_name: str
    last_name: str | None = None
    username: str | None = None
    photo_url: str | None = None
    birthday: date

class UserOut(UserBase):
    countdown: str