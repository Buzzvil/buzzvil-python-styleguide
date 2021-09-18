import ast

import pytest

from buzzvil_python_styleguide.plugin import FuncCallVisitor


class TestFucCallVisitor:
    @pytest.mark.parametrize(
        ('source', 'expected'),
        (
            ('request.test(1)', 'request.test'),
            ('test()', 'test'),
            ('some.long.function.call(123)', 'some.long.function.call'),
            ('some\\\n\t.long.function.call(123)', 'some.long.function.call'),
            ('some\\\n\t.long\\\n\t.function.call(123)', 'some.long.function.call'),
            ('some.long\\\n\t.function\\\n\t.call(123)', 'some.long.function.call'),
            ('request.post(\'some_url\', timeout=test())', 'request.post'),
            ('request.post(\'some_url\',\n\timeout=test()\n)', 'request.post'),
            ('request.get(\'some_url\',timeout=m.attr())', 'request.get'),
        ),
    )
    def test_name(self, source: str, expected: str) -> None:
        v = FuncCallVisitor()
        tree = ast.parse(source)
        v.visit(tree)
        assert expected == v.name
