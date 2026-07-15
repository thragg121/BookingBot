from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_admin_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📊 Statistics"),
                KeyboardButton(text="👥 Clients"),
            ],
            [
                KeyboardButton(text="🗓 Schedule"),
                KeyboardButton(text="⚙ Services"),
            ],
            [
                KeyboardButton(text="📢 Broadcast"),
                KeyboardButton(text="⬅ Back"),
            ],
        ],
        resize_keyboard=True,
    )
