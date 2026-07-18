from dataclasses import dataclass
from os import getenv

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True, slots=True)
class Config:
    bot_token: str
    database_url: str
    admin_ids: tuple[int, ...]
    working_days: tuple[int, ...]
    working_hour_start: int
    working_hour_end: int
    booking_days_ahead: int
    minimum_booking_notice_minutes: int
    booking_slot_interval_minutes: int


def _parse_int_tuple(
    value: str | None,
) -> tuple[int, ...]:
    if not value:
        return ()

    return tuple(
        int(item.strip())
        for item in value.split(",")
        if item.strip()
    )


def load_config() -> Config:
    bot_token = getenv("BOT_TOKEN", "").strip()

    if not bot_token:
        raise RuntimeError(
            "BOT_TOKEN is not set in the .env file."
        )

    database_url = getenv(
        "DATABASE_URL",
        "sqlite+aiosqlite:///data/booking.db",
    ).strip()

    working_days = _parse_int_tuple(
        getenv("WORKING_DAYS", "0,1,2,3,4")
    )

    working_hour_start = int(
        getenv("WORKING_HOUR_START", "9")
    )

    working_hour_end = int(
        getenv("WORKING_HOUR_END", "18")
    )

    booking_days_ahead = int(
        getenv("BOOKING_DAYS_AHEAD", "14")
    )

    minimum_booking_notice_minutes = int(
        getenv(
            "MINIMUM_BOOKING_NOTICE_MINUTES",
            "60",
        )
    )

    booking_slot_interval_minutes = int(
        getenv(
            "BOOKING_SLOT_INTERVAL_MINUTES",
            "60",
        )
    )

    if not working_days:
        raise RuntimeError(
            "WORKING_DAYS must contain at least one day."
        )

    if any(day < 0 or day > 6 for day in working_days):
        raise RuntimeError(
            "WORKING_DAYS values must be between 0 and 6."
        )

    if working_hour_start < 0 or working_hour_start > 23:
        raise RuntimeError(
            "WORKING_HOUR_START must be between 0 and 23."
        )

    if working_hour_end < 1 or working_hour_end > 24:
        raise RuntimeError(
            "WORKING_HOUR_END must be between 1 and 24."
        )

    if working_hour_start >= working_hour_end:
        raise RuntimeError(
            "WORKING_HOUR_START must be lower than WORKING_HOUR_END."
        )

    if booking_days_ahead < 1:
        raise RuntimeError(
            "BOOKING_DAYS_AHEAD must be greater than zero."
        )

    if minimum_booking_notice_minutes < 0:
        raise RuntimeError(
            "MINIMUM_BOOKING_NOTICE_MINUTES cannot be negative."
        )

    if booking_slot_interval_minutes < 5:
        raise RuntimeError(
            "BOOKING_SLOT_INTERVAL_MINUTES must be at least 5."
        )

    if booking_slot_interval_minutes > 720:
        raise RuntimeError(
            "BOOKING_SLOT_INTERVAL_MINUTES is too large."
        )

    return Config(
        bot_token=bot_token,
        database_url=database_url,
        admin_ids=_parse_int_tuple(
            getenv("ADMIN_IDS")
        ),
        working_days=working_days,
        working_hour_start=working_hour_start,
        working_hour_end=working_hour_end,
        booking_days_ahead=booking_days_ahead,
        minimum_booking_notice_minutes=(
            minimum_booking_notice_minutes
        ),
        booking_slot_interval_minutes=(
            booking_slot_interval_minutes
        ),
    )
