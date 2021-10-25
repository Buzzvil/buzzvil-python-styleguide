import ast
from typing import ClassVar, Iterable, Tuple, Type

import buzzvil_python_styleguide


def get_invocation_line(c: ast.Call) -> str:
    def dfs(a: ast.AST) -> str:
        child = getattr(a, 'value', None)
        name = getattr(a, 'id', getattr(a, 'attr', None))

        if child is None or not isinstance(child, ast.AST):
            if name is None or not isinstance(name, str):
                return ''
            return name

        return '.'.join(filter(None, (dfs(child), name)))

    return dfs(c.func)


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

            invocation_line = get_invocation_line(node)
            # There can be different ways of calling requests method but this covers almost all cases.
            if invocation_line not in ('requests.get', 'requests.post', 'session.get', 'session.post'):
                continue

            if 'timeout' not in [k.arg for k in node.keywords]:
                yield (
                    node.lineno,
                    node.col_offset,
                    'BZ1: timeout keyword is required for requests.get and requests.post',
                    type(self),
                )
