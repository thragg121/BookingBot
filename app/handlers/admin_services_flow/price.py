from decimal import Decimal, InvalidOperation

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.filters.admin import IsAdmin
from app.keyboards.admin_services import (
    get_services_admin_keyboard,
)
from app.services.service_admin import (
    change_service_price,
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
    F.data.startswith("edit_service_price:")
)
async def edit_service_price_handler(
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
        ServiceManagementState.waiting_for_price
    )

    if callback.message is not None:
        await callback.message.answer(
            f"💰 Current price for "
            f"<b>{service.name}</b>: "
            f"<b>${service.price:.2f}</b>\n\n"
            "Send the new price.\n"
            "Example: <code>45.50</code>"
        )

    await callback.answer()


@router.message(
    ServiceManagementState.waiting_for_price
)
async def new_service_price_handler(
    message: Message,
    session: AsyncSession,
    state: FSMContext,
) -> None:
    if not message.text:
        await message.answer(
            "Send the price as a number."
        )
        return

    normalized_price = (
        message.text
        .strip()
        .replace(",", ".")
        .replace("$", "")
    )

    try:
        price = Decimal(normalized_price)
    except InvalidOperation:
        await message.answer(
            "Invalid price.\n"
            "Example: <code>45.50</code>"
        )
        return

    if price <= 0:
        await message.answer(
            "The price must be greater than zero."
        )
        return

    if price > Decimal("999999.99"):
        await message.answer(
            "The price is too high."
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

    service = await change_service_price(
        session=session,
        service_id=int(service_id),
        price=price,
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
        f"✅ Price updated.\n\n"
        f"Service: <b>{service.name}</b>\n"
        f"New price: <b>${service.price:.2f}</b>",
        reply_markup=get_services_admin_keyboard(
            services
        ),
    )
