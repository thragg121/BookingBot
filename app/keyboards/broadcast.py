from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_broadcast_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Надіслати розсилку",
                    callback_data="broadcast_confirm",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="broadcast_cancel",
                ),
            ],
        ]
    )
