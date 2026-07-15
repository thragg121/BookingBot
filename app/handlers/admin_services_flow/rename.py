from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.keyboards.admin_services import get_services_admin_keyboard
from app.services.service_admin import (
    get_admin_service,
    list_services_for_admin,
    rename_admin_service,
)
from app.states.service_management import ServiceManagementState


router = Router()

router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.callback_query(
    F.data.startswith("rename_service:")
)
async def rename_service_start_handler(
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
    )

    await state.set_state(
        ServiceManagementState.waiting_for_rename
    )

    if callback.message is not None:
        await callback.message.answer(
            f"Current name: <b>{service.name}</b>\n\n"
            "Send the new service name."
        )

    await callback.answer()


@router.message(
    ServiceManagementState.waiting_for_rename
)
async def rename_service_finish_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    if not message.text:
        await message.answer(
            "Send the service name as text."
        )
        return

    new_name = message.text.strip()

    if len(new_name) < 2:
        await message.answer(
            "The service name is too short."
        )
        return

    if len(new_name) > 150:
        await message.answer(
            "The service name is too long."
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

    service = await rename_admin_service(
        session=session,
        service_id=int(service_id),
        new_name=new_name,
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
        "✅ Service renamed.\n\n"
        f"New name: <b>{service.name}</b>",
        reply_markup=get_services_admin_keyboard(
            services
        ),
    )
