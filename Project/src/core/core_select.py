from sqlalchemy import select

from core.core import products_table


def load_db():
    products = []; costs = []

    for register in select([products_table]).execute():
        _, product, cost, _ = register
        products.append(product)
        costs.append(cost)

    return products, costs
    