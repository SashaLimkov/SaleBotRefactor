import os
import sys

from ..easy_inline_kb.keyboard import EasyInlineKeyboard

import pytest

sys.path.insert(0, "%s/../" % os.path.dirname(os.path.abspath(__file__)))


def test_items_is_none_or_empty():
    """
    :return:
    """
    with pytest.raises(ValueError) as _:
        EasyInlineKeyboard(items=[])
    with pytest.raises(ValueError) as _:
        EasyInlineKeyboard(items=None)


def test_copy_text_to_callback_is_not_bool():
    """
    :return:
    """
    with pytest.raises(TypeError) as _:
        EasyInlineKeyboard(items=[1, 2, 3], copy_text_to_callback="text")


def test_number_of_items_out_of_limits():
    """
    :return:
    """
    with pytest.raises(ValueError) as _:
        EasyInlineKeyboard(items=list(range(200)), copy_text_to_callback=True)


def test_number_of_items_in_row_out_of_limits():
    """
    :return:
    """
    with pytest.raises(ValueError) as _:
        EasyInlineKeyboard(items=[[1, 2, 3], list(range(10))], copy_text_to_callback=True)
