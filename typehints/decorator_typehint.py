# from typing import ParamSpec, TypeVar
#
# Param = ParamSpec("Param")
# RetType = TypeVar("RetType")
#
# # def outer(func: Callable[Param, RetType]) -> Callable[Param, RetType]:
# #     @wraps(func)
# #     def inner(*args, **kwargs):
# #         print("pre decorator")
# #
# #         result = func(*args, **kwargs)
# #
# #         print("post decorator")
# #         return result
# #
# #     return inner
#
# from functools import wraps
# from typing import TypeVar
#
# T = TypeVar('T')
#
# from typing import Callable, TypeVar
# from time import time
#
# R = TypeVar("R")
# P = ParamSpec("P")
#
#
# def timethis(f: Callable[P, R]) -> Callable[P, R]:
#     def _inner(*args: P.args, **kwargs: P.kwargs) -> R:
#         start = time()
#         result = f(*args, **kwargs)
#
#         elapsed = time() - start
#         print(f"{f.__name__} calculate for {elapsed} seconds")
#         return result
#
#     return _inner
#
#
# def timethis2(f):
#     @wraps(f)
#     def _inner(*args, **kwargs):
#         start = time()
#         result = f(*args, **kwargs)
#         elapsed = time() - start
#         print(f"{f.__name__} calculate for {elapsed} seconds")
#         return result
#
#     return _inner
#
#
#
