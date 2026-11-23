from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.core.texts import format_price
from app.models.service import Service


def get_services_admin_keyboard(
    services: list[Service],
) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(
                text="➕ Додати послугу",
                callback_data="add_service",
            )
        ]
    ]

    for service in services:
        status = "🟢" if service.is_active else "🔴"

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=(
                        f"{status} {service.name} | "
                        f"{format_price(service.price)} | "
                        f"{service.duration_minutes} хв"
                    ),
                    callback_data=f"toggle_service:{service.id}",
                )
            ]
        )
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="✏ Назва",
                    callback_data=f"rename_service:{service.id}",
                ),
                InlineKeyboardButton(
                    text="💰 Ціна",
                    callback_data=f"edit_service_price:{service.id}",
                ),
            ]
        )
        keyboard.append(
            [
                InlineKeyboardButton(
                    text="⏱ Тривалість",
                    callback_data=f"edit_service_duration:{service.id}",
                ),
                InlineKeyboardButton(
                    text="🗑 Видалити",
                    callback_data=f"delete_service:{service.id}",
                ),
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
