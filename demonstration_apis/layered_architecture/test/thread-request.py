import requests

import threading


def worker():
    r = requests.get("http://127.0.0.1:8080/api/v1/member/1")


for x in range(3000):
    th1 = threading.Thread(target=worker)
    th1.start()
