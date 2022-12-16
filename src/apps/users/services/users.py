from typing import Union, List

from django.contrib.auth.models import User
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models import QuerySet


def get_search_users_queryset(search: str) -> Union[QuerySet, List[User]]:
    """Получить QuerySet сотрудников с поиском по строке search"""
    vector = TrigramSimilarity('phone', search) + TrigramSimilarity('username', search) \
                  + TrigramSimilarity('full_name', search)
    queryset = User.objects.annotate(similarity=vector).filter(
            similarity__gt=0.35).order_by('-similarity')
    return queryset


def get_all_users_queryset() -> Union[QuerySet, List[User]]:
    """Получить QuerySet сотрудников"""
    return User.objects.all()
