import asyncio

from app.bot import create_bot, create_dispatcher
from app.database.database import Database
from app.database.init_db import init_database
from app.database.seed import seed_services
from app.handlers.router import register_routers
from app.core.logger import logger
from app.middlewares.database import DatabaseMiddleware
from config import load_config


async def main() -> None:
    config = load_config()

    bot = create_bot(config)
    dp = create_dispatcher()
    database = Database(config)

    await init_database(database)
    await seed_services(database)

    dp.update.middleware(
        DatabaseMiddleware(database)
    )

    register_routers(dp)

    logger.info("BookingBot started.")

    try:
        await dp.start_polling(
    bot,
    config=config,
)
    finally:
        logger.info("BookingBot stopped.")
        await database.dispose()
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
