from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.models.service import Service


def get_services_admin_keyboard(
    services: list[Service],
) -> InlineKeyboardMarkup:
    keyboard: list[list[InlineKeyboardButton]] = []

    keyboard.append(
        [
            InlineKeyboardButton(
                text="➕ Add Service",
                callback_data="add_service",
            )
        ]
    )

    for service in services:
        status = "🟢" if service.is_active else "🔴"
        formatted_price = f"{service.price:.2f}"

        keyboard.append(
            [
                InlineKeyboardButton(
                    text=(
                        f"{status} {service.name} | "
                        f"${formatted_price} | "
                        f"{service.duration_minutes} min"
                    ),
                    callback_data=f"toggle_service:{service.id}",
                )
            ]
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    text="✏ Rename",
                    callback_data=f"rename_service:{service.id}",
                ),
                InlineKeyboardButton(
                    text="💰 Price",
                    callback_data=f"edit_service_price:{service.id}",
                ),
            ]
        )

        keyboard.append(
            [
                InlineKeyboardButton(
                    text="⏱ Duration",
                    callback_data=f"edit_service_duration:{service.id}",
                ),
                InlineKeyboardButton(
                    text="🗑 Delete",
                    callback_data=f"delete_service:{service.id}",
                ),
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=keyboard
    )
