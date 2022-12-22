from aiogram.dispatcher.filters.state import StatesGroup, State


class Currency(StatesGroup):
    GET_CUR_VALUE = State()
    MENU = State()
