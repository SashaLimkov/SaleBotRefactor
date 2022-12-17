import datetime
from typing import Union, List, Optional

from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet, Q

from apps.posts.models import Compilation, FinalCompilation


def get_list_compilations_by_date(
        date: datetime.date,
) -> Union[QuerySet, List[Compilation]]:
    """Возвращает QuerySet подборок, за выбранную дату"""
    return Compilation.objects.filter(date=date)


def get_compilation_by_id(compilation_id: int) -> Compilation:
    """Возвращает подборку по названию"""
    return Compilation.objects.filter(pk=compilation_id).first()


def get_search_compilations_queryset(search: str, filter_date: Q) -> Union[QuerySet, List[Compilation]]:
    """Получить QuerySet подборок с поиском по строке search"""
    vector = TrigramSimilarity('name', search) + TrigramSimilarity('text', search)
    if filter_date:
        queryset = Compilation.objects.prefetch_related('contents').annotate(similarity=vector).filter(
            filter_date, similarity__gt=0.35).order_by('-similarity')
    else:
        queryset = Compilation.objects.prefetch_related('contents').annotate(similarity=vector).filter(
            similarity__gt=0.35).order_by('-similarity')
    return queryset


def get_all_compilation_queryset(filter_date: Q) -> Union[QuerySet, List[Compilation]]:
    """Получить QuerySet пользователей"""
    if filter_date:
        return Compilation.objects.filter(filter_date).prefetch_related('contents')
    else:
        return Compilation.objects.all().prefetch_related('contents')


def get_date_range_compilation_filter(date_start: Optional[datetime.date],
                                      date_end: Optional[datetime.date]) -> Q:
    """Получение фильтра по дате создания подборки"""
    return Q(date__gte=date_start, date__lte=date_end)


def get_content_compilation_queryset(queryset: QuerySet) -> Union[QuerySet, List[Compilation]]:
    """Привязать поле с контентом к существующему QuerySet"""
    for item in queryset:
        if item.contents.all():
            item.media = item.contents.all()[0].file
    return queryset


def create_compilation(name: str, date: datetime.datetime, text: str,
                       done: bool, datetime_send: datetime.datetime) -> Compilation:
    """Создает новый объект подборки"""
    return Compilation.objects.create(
        name=name,
        text=text,
        date=date,
        datetime_send=datetime_send,
        done=done
    )


def update_compilation(compilation_id: int, name: str, date: datetime.datetime, text: str,
                       done: bool, datetime_send: datetime.datetime) -> Compilation:
    """Обновляет существующий объект подборки"""
    compilation = Compilation.objects.get(pk=compilation_id)
    compilation.name = name
    compilation.date = date
    compilation.done = done
    compilation.text = text
    compilation.datetime_send = datetime_send
    compilation.save()
    return compilation


def create_final_compilation(compilation_id: int, text: str) -> FinalCompilation:
    """Создает новый объект окончания подборки"""
    return FinalCompilation.objects.create(
        compilation_id=compilation_id,
        text=text,
    )


def update_or_create_final_compilation(compilation_id: int, text: str,) -> FinalCompilation:
    """Обновляет существующий объект окончания подборки"""
    return FinalCompilation.objects.update_or_create(compilation_id=compilation_id,
                                                     defaults={'text': text})

