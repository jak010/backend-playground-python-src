import threading
import time

from MySQLdb import Connection

from usages.database_usecase._initialize.notepad import generate_member_object


def save_member(members):
    connection = Connection(
        host='127.0.0.1',
        port=19501,
        user='root',
        passwd='1234',
        db='demo',
        charset='utf8'
    )
    cursor = connection.cursor()

    sql = "INSERT INTO demo.`member` (nanoid, name, age, address1, address2) VALUES  (%(nanoid)s, %(name)s, %(age)s, %(address1)s, %(address2)s)"
    cursor.executemany(sql, [
        {
            'nanoid': member.nanoid,
            'name': member.name,
            'age': member.age,
            'address1': member.address1,
            'address2': member.address2
        } for member in members
    ])
    connection.commit()
    connection.close()


def insert_member():
    members = generate_member_object()

    start_time = time.time()

    ths = []

    chunk_size = 10_000
    for i in range(0, len(members), chunk_size):
        member_chnuk = members[i:i + chunk_size]
        th = threading.Thread(target=save_member, args=(member_chnuk,))
        ths.append(th)
        th.start()

    for th in ths:
        th.join()

    print(time.time() - start_time)


if __name__ == '__main__':
    insert_member()
