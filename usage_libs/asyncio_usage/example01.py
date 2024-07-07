async def f():
    return 123


print(type(f))  # f() 라는 함수의 정확한 타입은 코루틴이 아니다. 일반적인 함수

import inspect

res = inspect.iscoroutinefunction(f)  # async def 라 붙은 함수를 코루틴이라 일컫지만 정확히는 "코루틴 함수"
print(res)
