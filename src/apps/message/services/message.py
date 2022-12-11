from typing import Optional

from apps.message.models import Message

from apps.profiles.services.profile import update_last_action_date_profile
from apps.profiles.services.subscription import get_user_active_subscription


def get_message_by_name_for_user(name: str, telegram_id: int = None) -> Message | bool:
    """Возвращает сообщение по название, обновляет метрики пользователя и
    проверяет существование активной подписки. В случае отсутствия подписки возвращает False"""
    if telegram_id:
        update_last_action_date_profile(telegram_id)
        if get_user_active_subscription(telegram_id):
            return _get_message_by_name(name)
        else:
            return False
    return _get_message_by_name(name)


def _get_message_by_name(name: str) -> Message:
    """Возвращает сообщение по названию"""
    return Message.objects.select_related('keyboard').prefetch_related('keyboard__button_set').filter(name=name).first()
