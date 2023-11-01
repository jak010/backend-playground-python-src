from design.database.libs.context import Context


class ProductEntity:

    def __init__(self, product_id, name):
        self.product_id = product_id
        self.name = name

        self._category = []

    def category(self):
        return self._category

    def set_category(self, category_id, name):
        self._category.append({
            "category_id": category_id,
            "name": name
        })

    def __repr__(self):
        newline = "\n"
        return f"\nProductEntity(\n" \
               f" product_id={self.product_id}\n" \
               f" name={self.name}\n" \
               f" categories=[{newline + ''.join([str(c) + newline for c in self._category])}])"


class ProductCategoryQuery:
    TABLE_NAME = "products_category"

    def __init__(self):
        self.context = Context()

    def insert(self, product_id: int, category_id: int):
        sql = f"INSERT INTO {self.TABLE_NAME} (product_id, category_id)" \
              f"VALUE ({product_id}, {category_id});"
        self.context.cursor.execute(sql)
        self.context.commit()
        self.context.close()

    def get_product_category(self, product_id: int):
        product_category_sql = f"SELECT" \
                               f" C.category_id, " \
                               f" name " \
                               f" FROM product_category" \
                               f" LEFT JOIN category as C ON C.category_id = product_category.category_id" \
                               f" WHERE product_category.product_id = {product_id};"
        self.context.cursor.execute(product_category_sql)
        _product_category = self.context.cursor.fetchall()

        self.context.commit()
        self.context.close()
        return _product_category

    def get_product_categorys(self, product_ids: list[int]):
        product_category_sql = f"SELECT" \
                               f" product_id," \
                               f" C.category_id, " \
                               f" name " \
                               f" FROM product_category" \
                               f" LEFT JOIN category as C ON C.category_id = product_category.category_id" \
                               f" WHERE product_category.product_id IN %(product_ids)s;"
        self.context.cursor.execute(product_category_sql, {"product_ids": product_ids})
        _product_category = self.context.cursor.fetchall()

        self.context.commit()
        self.context.close()
        return _product_category


class ProductQuery:
    TABLE_NAME = "products"

    def __init__(self):
        self.context = Context()

    def get_product(self, product_id=1):
        product_sql = f"SELECT * FROM {self.TABLE_NAME} WHERE product_id={product_id};"

        self.context.cursor.execute(product_sql)
        _product = self.context.cursor.fetchone()

        self.context.commit()
        self.context.close()

        return ProductEntity(product_id=_product['product_id'], name=_product["name"])

    def get_products(self, page, size):
        product_sql = f"SELECT * FROM {self.TABLE_NAME} LIMIT {size} OFFSET {(page - 1) * size};"

        self.context.cursor.execute(product_sql)
        objs = []
        for _product in self.context.cursor.fetchall():
            objs.append(ProductEntity(
                product_id=_product['product_id'],
                name=_product["name"]
            ))

        self.context.commit()
        self.context.close()

        return objs

    def get_product2(self, product_id=1):
        sql = "SELECT" \
              " *" \
              f" FROM {self.TABLE_NAME}" \
              f" LEFT JOIN product_category AS pc ON pc.product_id = {self.TABLE_NAME}.product_id" \
              f" WHERE {self.TABLE_NAME}.product_id = {product_id};"
        self.context.cursor.execute(sql)
        data = self.context.cursor.fetchall()
        self.context.commit()
        self.context.close()
        return data


if __name__ == '__main__':
    product = ProductQuery()
    product_category = ProductCategoryQuery()

    # one()
    # p = product.get_product(product_id=1)
    # p.set_category(categories=product_category.get_product_category(product_id=p.product_id))

    # all()
    products = product.get_products(page=1, size=100_000)
    product_categories = product_category.get_product_categorys(product_ids=[int(p.product_id) for p in products])

    from itertools import groupby


    def key_func(k):
        return k['product_id']


    print(len(products))
    print(len(product_categories))

    hmap = {k: list(v) for k, v in groupby(sorted(product_categories, key=key_func), key_func)}

    for product in products:
        if product.product_id in hmap:
            for category in hmap[product.product_id]:
                product.set_category(category_id=category['category_id'], name=category['name'])

    print(products)
