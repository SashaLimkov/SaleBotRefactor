from typing import Union, List

from django.db.models import QuerySet

from apps.settings.models import Currency


def get_list_currency() -> Union[QuerySet, List[Currency]]:
    """Возвращает список валют"""
    return Currency.objects.all()
