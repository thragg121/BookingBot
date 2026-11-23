from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.core.texts import format_price
from app.models.service import Service


def get_services_keyboard(
    services: list[Service],
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{service.name} — {format_price(service.price)}",
                callback_data=f"service:{service.id}",
            )
        ]
        for service in services
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)
