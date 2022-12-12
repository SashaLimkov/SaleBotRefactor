from .admin_filter import IsAdmin
from bot.config.loader import dp
from .registered_user_filter import IsRegistered, NotRegistered

if __name__ == "filters":
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsRegistered)
    dp.filters_factory.bind(NotRegistered)
