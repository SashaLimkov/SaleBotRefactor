from .admin_filter import IsAdmin
from bot.config.loader import dp

if __name__ == 'filters':
    dp.filters_factory.bind(IsAdmin)
