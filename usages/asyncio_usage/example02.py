async def f():
    return 123


coro = f()

try:
    coro.send(None)
except StopIteration as e:
    print("The Answer was:", e.value)
