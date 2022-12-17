from .admin_filter import IsAdmin
from bot.config.loader import dp
from .registered_user_filter import IsRegistered, NotRegistered
from .is_trial import IsTrial, IsNotTrial, IsHelper

if __name__ == "filters":
    dp.filters_factory.bind(IsAdmin)
    dp.filters_factory.bind(IsRegistered)
    dp.filters_factory.bind(NotRegistered)
    dp.filters_factory.bind(IsTrial)
    dp.filters_factory.bind(IsNotTrial)
    dp.filters_factory.bind(IsHelper)
