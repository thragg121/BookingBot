from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class Config:
    bot_token: str
    openai_api_key: str
    database_url: str
    admin_ids: tuple[int, ...]


def _parse_admin_ids(value: str | None) -> tuple[int, ...]:
    if not value:
        return ()

    return tuple(
        int(item.strip())
        for item in value.split(",")
        if item.strip()
    )


def load_config() -> Config:
    bot_token = getenv("BOT_TOKEN", "").strip()
    openai_api_key = getenv("OPENAI_API_KEY", "").strip()
    database_url = getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///data/booking.db",
    ).strip()
    admin_ids = _parse_admin_ids(getenv("ADMIN_IDS"))

    if not bot_token:
        raise RuntimeError("BOT_TOKEN is not set in the .env file.")

    return Config(
        bot_token=bot_token,
        openai_api_key=openai_api_key,
        database_url=database_url,
        admin_ids=admin_ids,
    )
