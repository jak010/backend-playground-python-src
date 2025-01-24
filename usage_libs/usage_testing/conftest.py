import pytest

from _pytest.reports import TestReport

# @pytest.hookimpl(hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     outcome = yield
#     report: TestReport = outcome.get_result()
#
#     test_fn = item.obj
#     docstring = getattr(test_fn, '__doc__')
#     if docstring:
#         report.location = docstring, 0, docstring
#         report.longreprtext = docstring

from _pytest.terminal import TerminalReporter


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        docstring = getattr(item.obj, '__doc__')
        print(f"::{docstring}")
        fixture_extras = getattr(item.config, "extras", [])
        plugin_extras = getattr(report, "extra", [])

        report.extra = fixture_extras + plugin_extras
