from aiogram.dispatcher.filters.state import StatesGroup, State


class Commission(StatesGroup):
    GET_COMMISSION = State()