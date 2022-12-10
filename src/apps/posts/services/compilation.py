import datetime
from typing import Union, List

from django.db.models import QuerySet

from apps.posts.models import Compilation


def get_list_compilations_by_date(date: datetime.date) -> Union[QuerySet, List[Compilation]]:
    """Возвращает QuerySet подборок, за выбранную дату"""
    return Compilation.objects.filter(date=date)


def get_compilation_by_id(compilation_id: int) -> Compilation:
    """Возвращает подборку по названию"""
    return Compilation.objects.get(pk=compilation_id)
