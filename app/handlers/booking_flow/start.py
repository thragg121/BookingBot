from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.texts import BTN_BOOK
from app.keyboards.services import get_services_keyboard
from app.services.booking_service import list_available_services
from app.states.booking import BookingState


router = Router()


@router.message(F.text == BTN_BOOK)
async def booking_start_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    services = await list_available_services(session)

    if not services:
        await message.answer(
            "Наразі немає доступних послуг."
        )
        return

    await state.clear()
    await state.set_state(
        BookingState.choosing_service
    )

    await message.answer(
        "💅 Оберіть послугу:",
        reply_markup=get_services_keyboard(services),
    )
