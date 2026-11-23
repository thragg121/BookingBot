from aiogram import Bot

from app.core.logger import logger
from config import Config


def _username_text(username: str | None) -> str:
    return f"@{username}" if username else "не вказано"


async def _send_to_admins(
    bot: Bot,
    config: Config,
    text: str,
    visitor_id: int,
) -> None:
    recipients = list(config.admin_ids)

    # In demo mode the visitor also receives the owner's notification,
    # so they can see exactly what the business owner gets.
    if config.demo_mode and visitor_id not in recipients:
        recipients.append(visitor_id)

    for chat_id in recipients:
        message_text = text

        if config.demo_mode and chat_id == visitor_id:
            message_text = (
                "👀 <i>Так це сповіщення бачить власник салону:</i>\n\n"
                + text
            )

        try:
            await bot.send_message(chat_id=chat_id, text=message_text)
        except Exception as error:
            logger.warning(
                "Failed to send notification to {}: {}", chat_id, error
            )


async def notify_admins_about_booking(
    bot: Bot,
    config: Config,
    user_id: int,
    first_name: str,
    username: str | None,
    booking_id: int,
    service_name: str,
    booking_date: str,
    booking_time: str,
    price: str,
) -> None:
    text = (
        "🔔 <b>Новий запис</b>\n\n"
        f"Запис №<code>{booking_id}</code>\n"
        f"Клієнт: <b>{first_name}</b>\n"
        f"Telegram: {_username_text(username)}\n\n"
        f"Послуга: <b>{service_name}</b>\n"
        f"Дата: <b>{booking_date}</b>\n"
        f"Час: <b>{booking_time}</b>\n"
        f"Вартість: <b>{price}</b>"
    )

    await _send_to_admins(bot, config, text, user_id)


async def notify_admins_about_cancellation(
    bot: Bot,
    config: Config,
    user_id: int,
    first_name: str,
    username: str | None,
    booking_id: int,
    service_name: str,
    booking_date: str,
    booking_time: str,
) -> None:
    text = (
        "❌ <b>Запис скасовано</b>\n\n"
        f"Запис №<code>{booking_id}</code>\n"
        f"Клієнт: <b>{first_name}</b>\n"
        f"Telegram: {_username_text(username)}\n\n"
        f"Послуга: <b>{service_name}</b>\n"
        f"Дата: <b>{booking_date}</b>\n"
        f"Час: <b>{booking_time}</b>\n\n"
        "<i>Вікно знову вільне для інших клієнтів.</i>"
    )

    await _send_to_admins(bot, config, text, user_id)
