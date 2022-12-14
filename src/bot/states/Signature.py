from aiogram.dispatcher.filters.state import StatesGroup, State


class Signature(StatesGroup):
    GET_SIGNATURE = State()