from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.keyboards.admin_services import (
    get_services_admin_keyboard,
)
from app.services.service_admin import (
    change_service_duration,
    get_admin_service,
    list_services_for_admin,
)
from app.states.service_management import (
    ServiceManagementState,
)


router = Router()

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(
    F.data.startswith("edit_service_duration:")
)
async def edit_service_duration_handler(
    callback: CallbackQuery,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    if callback.data is None:
        return

    service_id = int(
        callback.data.split(":", maxsplit=1)[1]
    )

    service = await get_admin_service(
        session=session,
        service_id=service_id,
    )

    if service is None:
        await callback.answer(
            "Service not found.",
            show_alert=True,
        )
        return

    await state.update_data(
        service_id=service.id,
        service_name=service.name,
    )

    await state.set_state(
        ServiceManagementState.waiting_for_duration
    )

    if callback.message is not None:
        await callback.message.answer(
            f"⏱ Current duration for "
            f"<b>{service.name}</b>: "
            f"<b>{service.duration_minutes} minutes</b>\n\n"
            "Send the new duration in minutes.\n"
            "Example: <code>60</code>"
        )

    await callback.answer()


@router.message(
    ServiceManagementState.waiting_for_duration
)
async def new_service_duration_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    if not message.text:
        await message.answer(
            "Send the duration as a whole number."
        )
        return

    try:
        duration_minutes = int(message.text.strip())
    except ValueError:
        await message.answer(
            "Invalid duration.\n"
            "Example: <code>60</code>"
        )
        return

    if duration_minutes < 5:
        await message.answer(
            "Duration must be at least 5 minutes."
        )
        return

    if duration_minutes > 1440:
        await message.answer(
            "Duration cannot exceed 1440 minutes."
        )
        return

    state_data = await state.get_data()
    service_id = state_data.get("service_id")

    if service_id is None:
        await state.clear()
        await message.answer(
            "Service data is missing. Try again."
        )
        return

    service = await change_service_duration(
        session=session,
        service_id=int(service_id),
        duration_minutes=duration_minutes,
    )

    if service is None:
        await state.clear()
        await message.answer(
            "Service not found."
        )
        return

    await state.clear()

    services = await list_services_for_admin(session)

    await message.answer(
        f"✅ Duration updated.\n\n"
        f"Service: <b>{service.name}</b>\n"
        f"New duration: "
        f"<b>{service.duration_minutes} minutes</b>",
        reply_markup=get_services_admin_keyboard(
            services
        ),
    )
