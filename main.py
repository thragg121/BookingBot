import asyncio
import os

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter

from app.bot import create_bot, create_dispatcher
from app.database.database import Database
from app.database.init_db import init_database
from app.database.seed import seed_services
from app.handlers.router import register_routers
from app.core.logger import logger
from app.middlewares.database import DatabaseMiddleware
from config import load_config


async def wait_for_telegram(bot: Bot) -> None:
    """Resolve the bot identity, honouring Telegram flood-control waits.

    Crashing on TelegramRetryAfter makes the host restart the process
    immediately, which triggers another GetMe call and extends the ban.
    bot.me() caches the result, so start_polling will not call GetMe again.
    """
    while True:
        try:
            me = await bot.me()
            logger.info("Connected to Telegram as @{}", me.username)
            return
        except TelegramRetryAfter as error:
            delay = error.retry_after + 1
            logger.warning(
                "Telegram flood control: waiting {} seconds before retry.",
                delay,
            )
            await asyncio.sleep(delay)


async def main() -> None:
    config = load_config()

    # SQLite needs its folder to exist (e.g. data/ on a fresh server).
    if config.database_url.startswith("sqlite"):
        db_path = config.database_url.split(":///", 1)[-1]
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

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
        await wait_for_telegram(bot)
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
