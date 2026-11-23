from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.core.texts import (
    BTN_BACK,
    BTN_BROADCAST,
    BTN_CLIENTS,
    BTN_SCHEDULE,
    BTN_SERVICES,
    BTN_STATS,
)


def get_admin_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=BTN_STATS),
                KeyboardButton(text=BTN_CLIENTS),
            ],
            [
                KeyboardButton(text=BTN_SCHEDULE),
                KeyboardButton(text=BTN_SERVICES),
            ],
            [
                KeyboardButton(text=BTN_BROADCAST),
                KeyboardButton(text=BTN_BACK),
            ],
        ],
        resize_keyboard=True,
    )
