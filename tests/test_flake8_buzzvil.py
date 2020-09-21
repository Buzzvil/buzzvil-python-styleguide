# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

from buzzvil_python_styleguide import __version__


def test_version() -> None:
    assert __version__ == '0.1.0'
