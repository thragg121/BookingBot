from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Book Appointment")],
            [KeyboardButton(text="📖 My Bookings")],
            [KeyboardButton(text="🤖 AI Assistant")],
            [KeyboardButton(text="👤 Profile")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Choose an action...",
    )
