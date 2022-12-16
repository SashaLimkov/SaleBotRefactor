import datetime
from typing import Union, List

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet

from apps.posts.models import Compilation


def get_list_compilations_by_date(
        date: datetime.date,
) -> Union[QuerySet, List[Compilation]]:
    """Возвращает QuerySet подборок, за выбранную дату"""
    return Compilation.objects.filter(date=date)


def get_compilation_by_id(compilation_id: int) -> Compilation:
    """Возвращает подборку по названию"""
    return Compilation.objects.filter(pk=compilation_id).first()


def get_search_compilations_queryset(search: str) -> Union[QuerySet, List[Compilation]]:
    """Получить QuerySet подборок с поиском по строке search"""
    vector = TrigramSimilarity('phone', search) + TrigramSimilarity('username', search) \
             + TrigramSimilarity('full_name', search)
    queryset = Compilation.objects.prefetch_related('contents').annotate(similarity=vector).filter(
        similarity__gt=0.35).order_by('-similarity')
    return queryset


def get_all_compilation_queryset() -> Union[QuerySet, List[Compilation]]:
    """Получить QuerySet пользователей"""
    return Compilation.objects.all().prefetch_related('contents')


def get_content_compilation_queryset(queryset: QuerySet) -> Union[QuerySet, List[Compilation]]:
    """Привязать поле с контентом к существующему QuerySet"""
    for item in queryset:
        if item.contents.all():
            item.media = item.contents.all()[0].file
            print(item.media.url)
    return queryset
