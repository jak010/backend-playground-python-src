import pymysql
import uuid

from libs.context import Context

context = Context()

context.cursor.execute("TRUNCATE category;")

for _ in range(25):
    category_insert_sql = f"INSERT INTO playground.category (name) VALUES('{str(uuid.uuid4())[0:4]}');"
    context.cursor.execute(query=category_insert_sql)

context.commit()
context.close()
