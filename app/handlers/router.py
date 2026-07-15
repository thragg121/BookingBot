from aiogram import Dispatcher

from app.handlers.admin import router as admin_router
from app.handlers.admin_services_flow import (
    router as admin_services_flow_router,
)
from app.handlers.booking_flow import (
    router as booking_flow_router,
)
from app.handlers.broadcast import router as broadcast_router
from app.handlers.errors import router as errors_router
from app.handlers.profile import router as profile_router
from app.handlers.start import router as start_router
from app.handlers.system import router as system_router


def register_routers(dp: Dispatcher) -> None:
    dp.include_router(start_router)
    dp.include_router(system_router)
    dp.include_router(booking_flow_router)
    dp.include_router(profile_router)
    dp.include_router(admin_router)
    dp.include_router(admin_services_flow_router)
    dp.include_router(broadcast_router)
    dp.include_router(errors_router)
