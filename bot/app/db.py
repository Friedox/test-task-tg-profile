from tortoise import Tortoise, run_async
from bot.app.config import settings


async def init_db():
    await Tortoise.init(
        db_url=settings.database_url,
        modules={"models": ["models"]}
    )
    await Tortoise.generate_schemas()


if __name__ == "__main__":
    run_async(init_db())
