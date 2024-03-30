import threading
import time


class OtherBackgroundProcessThread(threading.Thread):
    daemon = True

    def run(self):
        while True:
            time.sleep(1)
            print("Thread")
