from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


AUDIENCE_ALL = "all"
AUDIENCE_BOOKED = "booked"


def get_broadcast_audience_keyboard(
    all_count: int,
    booked_count: int,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"👥 Усім клієнтам ({all_count})",
                    callback_data=f"broadcast_aud:{AUDIENCE_ALL}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text=f"📅 Тим, хто має запис ({booked_count})",
                    callback_data=f"broadcast_aud:{AUDIENCE_BOOKED}",
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
