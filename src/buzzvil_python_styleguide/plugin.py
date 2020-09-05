# coding: UTF-8
from __future__ import absolute_import, division, print_function, unicode_literals

import ast
from collections import deque

import buzzvil_python_styleguide


class FuncCallVisitor(ast.NodeVisitor):
    def __init__(self):
        self._name = deque()

    @property
    def name(self):
        return '.'.join(self._name)

    @name.deleter
    def name(self):
        self._name.clear()

    def visit_Name(self, node):  # noqa: N802
        self._name.appendleft(node.id)

    def visit_Attribute(self, node):  # noqa: N802
        try:
            self._name.appendleft(node.attr)
            self._name.appendleft(node.value.id)
        except AttributeError:
            self.generic_visit(node)


class RequestsTimeoutPlugin(object):
    name = buzzvil_python_styleguide.__name__
    version = buzzvil_python_styleguide.__version__

    def __init__(self, tree):
        self.tree = tree

    def run(self):
        """
        :return: (lineno, col_offset, error_string, Type)
        """
        for node in ast.walk(self.tree):
            if not isinstance(node, ast.Call):
                continue

            callvisitor = FuncCallVisitor()
            callvisitor.visit(node.func)
            # There can be different ways of calling requests method but this covers almost all cases.
            if callvisitor.name not in ('requests.get', 'requests.post', 'session.get', 'session.post'):
                continue

            if 'timeout' not in [k.arg for k in node.keywords]:
                yield (
                    node.lineno,
                    node.col_offset,
                    'BZ1: timeout keyword is required for requests.get and requests.post',
                    type(self),
                )
