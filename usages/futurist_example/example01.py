import time
from futurist import periodics


@periodics.periodic(1)
def every_one(stared_at):
    print("1: %s" % (time.time() - stared_at))


w = periodics.PeriodicWorker(
    [
        (every_one, (time.time(),), {})
    ]
)


@periodics.periodic(4)
def print_status():
    print("stat:%s" % list(w.iter_watchers()))


w.add(print_status)
w.start()
