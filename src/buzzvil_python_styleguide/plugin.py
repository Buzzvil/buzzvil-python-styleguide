import ast
from collections import deque
from typing import ClassVar, Deque, Iterable, Tuple, Type

import buzzvil_python_styleguide


class FuncCallVisitor(ast.NodeVisitor):
    _name: Deque[str]

    def __init__(self) -> None:
        self._name = deque()

    @property
    def name(self) -> str:
        return '.'.join(self._name)

    @name.deleter
    def name(self) -> None:
        self._name.clear()

    def visit_Name(self, node: ast.Name) -> None:  # noqa: N802
        self._name.appendleft(node.id)

    def visit_Attribute(self, node: ast.Attribute) -> None:  # noqa: N802
        self._name.appendleft(node.attr)
        if isinstance(node.value, ast.Name):
            self._name.appendleft(node.value.id)
        else:
            self.generic_visit(node)


class RequestsTimeoutPlugin:
    name: ClassVar[str] = buzzvil_python_styleguide.__name__
    version: ClassVar[str] = buzzvil_python_styleguide.__version__

    tree: ast.AST

    def __init__(self, tree: ast.AST) -> None:
        self.tree = tree

    def run(self) -> Iterable[Tuple[int, int, str, Type['RequestsTimeoutPlugin']]]:
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
