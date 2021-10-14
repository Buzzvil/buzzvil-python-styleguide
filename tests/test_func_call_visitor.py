import ast

import pytest

from buzzvil_python_styleguide.plugin import FuncCallVisitor, RequestsTimeoutPlugin


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


class TestRequestsTimeoutPlugin:
    _ERR_MSG = 'BZ1: timeout keyword is required for requests.get and requests.post'

    @pytest.mark.parametrize(
        ('invocation_line', 'is_lint_target'),
        (
            ('requests.post', True),
            ('requests.get', True),
            ('session.post', True),
            ('session.get', True),
            ('requests\\\n\t.get', True),
            ('requests.\\\n\tget', True),
            ('request.post', False),
            ('request.get', False),
        ),
    )
    @pytest.mark.parametrize(
        ('source', 'expected'),
        (
            (
                '{invocation_line}(\'some_url\', timeout=test())',
                (),
            ),
            (
                '{invocation_line}(\'some_url\')',
                ((1, 0, _ERR_MSG, RequestsTimeoutPlugin),),
            ),
            (
                'x = {invocation_line}(\'some_url\')',
                ((1, 4, _ERR_MSG, RequestsTimeoutPlugin),),
            ),
            (
                'with {invocation_line}(\'some_url\') as res:\n  pass',
                ((1, 5, _ERR_MSG, RequestsTimeoutPlugin),),
            ),
            (
                'with {invocation_line}(\'some_url\', timeout=test()) as res:\n  pass',
                (),
            ),
        ),
    )
    def test_run(self, invocation_line, is_lint_target, source, expected):
        tree = ast.parse(source.format(invocation_line=invocation_line))
        p = RequestsTimeoutPlugin(tree)
        if is_lint_target:
            assert expected == tuple(p.run())
        else:
            assert tuple() == tuple(p.run())
