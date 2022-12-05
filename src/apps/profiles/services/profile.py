from apps.profiles.models import Profile
from apps.utils.services.date_time import get_datetime_now


def create_profile(telegram_id: int, username: str = None, first_name: str = None, last_name: str = None) -> Profile:
    """Создание профиля пользователя бота"""
    return Profile.objects.create(telegram_id=telegram_id,
                                  username=username,
                                  first_name=first_name,
                                  last_name=last_name)


def get_profile_by_telegram_id(telegram_id: int) -> Profile:
    """Возвращает Profile пользователя по telegram_id"""
    return Profile.objects.get(telegram_id=telegram_id)


def update_last_action_date_profile(telegram_id: int) -> None:
    """Обновляет время последнего действия пользователя и инкрементирует количество действий"""
    profile = Profile.objects.get(telegram_id=telegram_id)
    profile.last_action_date = get_datetime_now()
    profile.count_actions_in_current_day += 1
    profile.save()
