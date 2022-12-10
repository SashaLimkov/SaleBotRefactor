from typing import Union, List

from django.db.models import QuerySet

from apps.settings.models import ChanelVk, ChanelTelegram


def get_list_telegram_channels(telegram_id: int) -> Union[QuerySet, List[ChanelTelegram]]:
    """Возвращает список каналов пользователя в Telegram"""
    return ChanelTelegram.objects.filter(profile_id=telegram_id).select_related('profile')


def get_list_vk_channels(telegram_id: int) -> Union[QuerySet, List[ChanelVk]]:
    """Возвращает список каналов пользователя в VK"""
    return ChanelVk.objects.filter(profile_id=telegram_id).select_related('profile')


def add_channel_telegram(telegram_id: int, name: str, channel_id: int) -> ChanelTelegram:
    """Создает новый Telegram канал пользователя"""
    return ChanelTelegram.objects.get_or_create(profile_id=telegram_id, name=name, chat_id=channel_id)


def add_channel_vk(telegram_id: int, channel_id: int) -> ChanelVk:
    """Создает новый VK канал пользователя"""
    return ChanelVk.objects.get_or_create(profile_id=telegram_id, chat_id=channel_id)


def delete_channel_telegram(telegram_id: int, channel_id: int) -> None:
    """Удаляет Telegram канал пользователя"""
    ChanelTelegram.objects.get(profile_id=telegram_id, chat_id=channel_id).delete()


def delete_channel_vk(telegram_id: int, channel_id: int) -> None:
    """Удаляет VK канал пользователя"""
    ChanelVk.objects.get(profile_id=telegram_id, chat_id=channel_id).delete()
