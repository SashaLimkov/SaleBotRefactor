from apps.message.models import Message

from apps.profiles.services.profile import update_last_action_date_profile


def get_message_by_name_for_user(name: str, telegram_id: int = None) -> Message:
    """Возвращает сообщение по название и обновляет метрики пользователя"""
    if telegram_id:
        update_last_action_date_profile(telegram_id)
    return _get_message_by_name(name)


def _get_message_by_name(name: str) -> Message:
    """Возвращает сообщение по названию"""
    return Message.objects.select_related('keyboard').prefetch_related('keyboard__button_set').get(name=name)
