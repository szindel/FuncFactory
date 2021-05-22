import pytest
from funcfactory import FuncFactory


def test_init_funcfactory():

    ff = FuncFactory(folder_results="./logs", list_modules_functions=None, get_logger=None)
    assert ff