from aiogram.dispatcher.filters.state import StatesGroup, State


class PostStates(StatesGroup):
    GET_TEXT = State()
