from core.core import products_table, engine

products = [
    {"product": "hipercalorico", "price": 75., "quantity": "3kg"},
    {"product": "leite_em_po", "price": 12.99, "quantity": "400g"},
    {"product": "arrozina", "price": 4.49, "quantity": "180g"},
    {"product": "file_de_frango", "price": 15.5, "quantity": "1kg"},
]

with engine.begin() as connection:
    connection.execute(
        products_table.insert(),
        products
    )
