from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.keyboards.admin_services import (
    get_services_admin_keyboard,
)
from app.services.service_admin import (
    list_services_for_admin,
)


router = Router()

router.message.filter(IsAdmin())


@router.message(F.text == "⚙ Services")
async def services_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    await state.clear()

    services = await list_services_for_admin(session)

    if not services:
        await message.answer(
            "No services have been created yet."
        )
        return

    await message.answer(
        "⚙ <b>Manage Services</b>\n\n"
        "Tap a service to enable or disable it.\n"
        "Use the buttons below to edit its settings.",
        reply_markup=get_services_admin_keyboard(
            services
        ),
    )
