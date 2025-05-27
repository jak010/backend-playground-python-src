import time
from multiprocessing import Process
from MySQLdb import Connection

from usages.database_usecase._initialize.notepad import generate_member_object
import pandas as pd


def insert_member():
    members = generate_member_object()

    member_df = pd.DataFrame([member.to_dict() for member in members])
    member_df.to_csv("./member.csv", index=False)

    import time
    start_time = time.time()
    connection = Connection(
        host='127.0.0.1',
        port=19501,
        user='root',
        passwd='1234',
        db='demo',
        charset='utf8',
        local_infile=1  # 중요
    )
    cursor = connection.cursor()

    sql = "LOAD DATA LOCAL INFILE './member.csv' INTO TABLE member FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n' IGNORE 1 LINES;"
    cursor.execute(sql)
    connection.commit()

    cursor.close()
    connection.close()

    print(time.time() - start_time)

if __name__ == '__main__':
    insert_member()
