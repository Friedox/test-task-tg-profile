from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import user, share
from app.config import settings
from tortoise.contrib.fastapi import register_tortoise
import uvicorn

app = FastAPI(
    title="Telegram Profile API",
    description="Backend service for managing Telegram user profiles and birthdays 🎉",
    version="1.0.0",
    contact={
        "name": "Dmitry",
        "url": "https://github.com/Friedox",
        "email": "dvzvidrin48@gmail.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api")
app.include_router(share.router, prefix="/api")

register_tortoise(
    app,
    db_url=settings.db_url,
    modules={"models": ["app.models.user"]},
    generate_schemas=True,
    add_exception_handlers=True
)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
