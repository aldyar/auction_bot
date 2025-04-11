from aiogram.fsm.state import StatesGroup, State


class InvalidBid(StatesGroup):
    text = State()

class Admin(StatesGroup):
    wait_username = State()

class User(StatesGroup):
    wait_add_sum = State()