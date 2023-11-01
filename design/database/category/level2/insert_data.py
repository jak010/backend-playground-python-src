import pymysql
import uuid
import random
from design.database.libs.context import Context

context = Context()

PRODUCT_LIMIT = 100_000
PRODUCT_CATEGORY_LIMIT = 100_000
CATEGORY = ["A", "B", "C", "D", "E"]

context.cursor.execute("TRUNCATE products;")
products_insert_sql = f"INSERT INTO playground.products (name) VALUES (%s);"
context.cursor.executemany(products_insert_sql, [str(uuid.uuid4())[0:4] for _ in range(PRODUCT_LIMIT)])
context.commit()

context.cursor.execute("TRUNCATE category;")
for _ in ["A", "B", "C", "D", "E"]:
    products_insert_sql = f"INSERT INTO playground.category (name) VALUES('{_}');"
    context.cursor.execute(query=products_insert_sql)
context.commit()

context.cursor.execute("TRUNCATE product_category;")
for x in range(PRODUCT_CATEGORY_LIMIT):
    random_product_id = random.randint(1, PRODUCT_LIMIT)
    random_category_id = random.randint(1, 5)

    try:
        products_insert_sql = f"INSERT IGNORE INTO playground.product_category (product_id, category_id)" \
                              f" VALUES({random_product_id},{random_category_id});"
        context.cursor.execute(query=products_insert_sql)
    except pymysql.err.InternalError:
        continue

context.commit()
context.close()
