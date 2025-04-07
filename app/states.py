from aiogram.fsm.state import StatesGroup, State


class InvalidBid(StatesGroup):
    text = State()

