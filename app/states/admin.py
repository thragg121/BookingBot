from aiogram.fsm.state import State, StatesGroup


class BroadcastState(StatesGroup):
    choosing_audience = State()
    waiting_for_message = State()
    confirming = State()
