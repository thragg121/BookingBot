from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.keyboards.services import get_services_keyboard
from app.services.booking_service import list_available_services
from app.states.booking import BookingState


router = Router()


@router.message(F.text == "📅 Book Appointment")
async def booking_start_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    services = await list_available_services(session)

    if not services:
        await message.answer(
            "No services are available right now."
        )
        return

    await state.clear()
    await state.set_state(
        BookingState.choosing_service
    )

    await message.answer(
        "Choose a service:",
        reply_markup=get_services_keyboard(services),
    )
