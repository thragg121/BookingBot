from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.services import get_active_services
from app.keyboards.dates import get_dates_keyboard
from app.states.booking import BookingState


router = Router()


@router.callback_query(
    BookingState.choosing_service,
    F.data.startswith("service:"),
)
async def service_selected_handler(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
) -> None:
    if callback.data is None:
        return

    service_id = int(
        callback.data.split(":", maxsplit=1)[1]
    )

    services = await get_active_services(session)

    service = next(
        (
            item
            for item in services
            if item.id == service_id
        ),
        None,
    )

    if service is None:
        await callback.answer(
            "Service not found.",
            show_alert=True,
        )
        return

    formatted_price = f"{service.price:.2f}"

    await state.update_data(
        service_id=service.id,
        service_name=service.name,
        service_price=formatted_price,
        duration_minutes=service.duration_minutes,
    )

    await state.set_state(
        BookingState.choosing_date
    )

    if callback.message is not None:
        await callback.message.edit_text(
            f"Selected service: <b>{service.name}</b>\n"
            f"Price: <b>${formatted_price}</b>\n"
            f"Duration: "
            f"<b>{service.duration_minutes} minutes</b>\n\n"
            "Choose a date:",
            reply_markup=get_dates_keyboard(),
        )

    await callback.answer()
