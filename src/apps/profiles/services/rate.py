from apps.profiles.models import Rate
from typing import Union, List
from django.db.models import QuerySet


def get_list_rates() -> Union[QuerySet, List[Rate]]:
    """Возвращает список всех существующих тарифов"""
    return Rate.objects.all()


def get_rate_by_pk(rate_pk: int) -> Rate:
    return Rate.objects.filter(pk=rate_pk).first()


def get_helper_rate_by_price(price: float) -> Rate:
    return Rate.objects.filter(price=price).first()
