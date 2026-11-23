from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_booking_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Підтвердити запис",
                    callback_data="booking_confirm",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❌ Скасувати",
                    callback_data="booking_cancel",
                ),
            ],
        ]
    )
