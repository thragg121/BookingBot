from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_booking_confirmation_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="? Confirm Booking",
                    callback_data="booking_confirm",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="? Cancel",
                    callback_data="booking_cancel",
                ),
            ],
        ]
    )
