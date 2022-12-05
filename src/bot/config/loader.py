"""Инициализирует все необходимые компоненты бота"""

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from django.conf import settings

bot = Bot(token=settings.BOT_TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
user_data = {}