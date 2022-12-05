from aiogram import Dispatcher
from bot.handlers import main


def setup(dp: Dispatcher):
    main.setup(dp)
