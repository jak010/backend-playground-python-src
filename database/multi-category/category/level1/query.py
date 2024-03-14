import pymysql
import uuid

from libs.context import Context

context = Context()

context.cursor.execute(
    "SELECT"
    " * "
    " FROM products"
    " LEFT JOIN category AS c ON c.category_id = products.category_id"
    " WHERE products.category_id=1;"

)

data = context.cursor.fetchone()

print(data)

context.commit()
context.close()
