from apps.profiles.models import Rate
from typing import Union, List
from django.db.models import QuerySet


def get_list_rates() -> Union[QuerySet, List[Rate]]:
    """Возвращает список всех существующих тарифов"""
    return Rate.objects.all()
