from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from app.core.texts import (
    BTN_BOOK,
    BTN_MY_BOOKINGS,
    BTN_OWNER_PANEL,
    BTN_PROFILE,
)


def get_main_menu(demo_mode: bool = False) -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=BTN_BOOK)],
        [
            KeyboardButton(text=BTN_MY_BOOKINGS),
            KeyboardButton(text=BTN_PROFILE),
        ],
    ]

    if demo_mode:
        keyboard.append([KeyboardButton(text=BTN_OWNER_PANEL)])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Оберіть дію...",
    )
