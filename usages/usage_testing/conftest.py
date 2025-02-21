# import pytest

# from _pytest.reports import TestReport
# from _pytest.fixtures import FuncFixtureInfo
from _pytest.python import Function


# # @pytest.hookimpl(hookwrapper=True)
# # def pytest_runtest_makereport(item, call):
# #     outcome = yield
# #     report: TestReport = outcome.get_result()
# #
# #     test_fn = item.obj
# #     docstring = getattr(test_fn, '__doc__')
# #     if docstring:
# #         report.location = docstring, 0, docstring
# #         report.longreprtext = docstring
#
# from _pytest.terminal import TerminalReporter
#
#
# # @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# # def pytest_runtest_makereport(item, call):
# #     outcome = yield
# #     report: TestReport = outcome.get_result()
# #     import sys
# #
# #     if report.when == "call":
# #         docstring = getattr(item.obj, '__doc__')
# #         report.nodeid = docstring

def pytest_itemcollected(item: Function):
    """ change test name, using fixture names """

    target_object = item._obj
    if target_object:
        item._nodeid = f"{item.nodeid}:{getattr(target_object, '__doc__')}"
    if target_object is None:
        raise Exception("target_object is None")
