from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_broadcast_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Send Broadcast",
                    callback_data="broadcast_confirm",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❌ Cancel",
                    callback_data="broadcast_cancel",
                ),
            ],
        ]
    )
