import pymysql
import uuid

from design.database.libs.context import Context

context = Context()

context.cursor.execute("TRUNCATE products;")

for _ in range(25):
    products_insert_sql = f"INSERT INTO playground.products (name) VALUES('{str(uuid.uuid4())[0:4]}');"
    context.cursor.execute(query=products_insert_sql)

context.commit()
context.close()
