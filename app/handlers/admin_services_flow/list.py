from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.texts import BTN_SERVICES
from app.filters.admin import IsAdmin
from app.keyboards.admin_services import (
    get_services_admin_keyboard,
)
from app.services.service_admin import (
    list_services_for_admin,
)


router = Router()

router.message.filter(IsAdmin())


@router.message(F.text == BTN_SERVICES)
async def services_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    await state.clear()

    services = await list_services_for_admin(session)

    if not services:
        await message.answer(
            "Послуг ще немає."
        )
        return

    await message.answer(
        "⚙ <b>Керування послугами</b>\n\n"
        "Натисніть на послугу, щоб увімкнути чи вимкнути її.\n"
        "Кнопки нижче змінюють назву, ціну та тривалість.",
        reply_markup=get_services_admin_keyboard(
            services
        ),
    )
