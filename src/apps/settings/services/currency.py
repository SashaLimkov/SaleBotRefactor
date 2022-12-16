from typing import Union, List

from django.db.models import QuerySet

from apps.settings.models import Currency

import xml.etree.ElementTree as ET

import requests


def get_course_currency(currency_name: str) -> float:
    """Возвращает курс валюты относительно рубля"""
    tree = ET.fromstring(requests.get("http://www.cbr.ru/scripts/XML_daily.asp").text)
    return float(
        tree.find(f"Valute[CharCode='{currency_name}']")
        .find("Value")
        .text.replace(",", ".")
    )


def get_list_currency() -> Union[QuerySet, List[Currency]]:
    """Возвращает список валют"""
    return Currency.objects.all()
