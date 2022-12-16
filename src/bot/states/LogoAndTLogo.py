from aiogram.dispatcher.filters.state import StatesGroup, State


class LogoAndTLogo(StatesGroup):
    EDIT_TEXT_LOGO = State()
    EDIT_LOGO = State()
