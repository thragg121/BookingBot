from aiogram.fsm.state import State, StatesGroup


class ServiceManagementState(StatesGroup):
    waiting_for_price = State()
    waiting_for_duration = State()
    waiting_for_rename = State()

    waiting_for_name = State()
    waiting_for_description = State()
    waiting_for_new_duration = State()
    waiting_for_new_price = State()
