from create_db import market_basket_table, engine


def load(market, product, price, quantity, measurement):
    return {
        "market": market,
        "product": product,
        "price": price,
        "quantity": quantity,
        "measurement": measurement
    }


datas = []

registers = (
    ("Multimix", "arroz", 31.0, 5, "kg"),
    ("Multimix", "macarrao", 3.38, 500, "g"),
    ("Multimix", "macarrao", 4.89, 1, "kg"),
    ("Multimix", "frango", 13.99, 1, "kg"),
    ("Multimix", "leite", 4.79, 1, "L"),
    ("Multimix", "pao", 7.49, 500, "g"),
    ("Multimix", "adocante", 6.79, 100, "ml"),
    ("Multimix", "feijao", 7.99, 1, "kg"),
    ("Multimix", "oleo", 8.49, 900, "ml"),
    ("Multimix", "acucar", 3.39, 1, "kg"),
    ("Multimix", "aveia", 9.69, 450, "g"),
    ("Multimix", "aveia", 6.99, 200, "g"),
    ("Multimix", "cafe", 9.99, 500, "g"),
    ("Loja de acai", "acai", 10.0, 1, "kg"),
    ("Tere 1", "ovo", 12.99, 30, "unid"),
    ("Tere 1", "arroz", 18.98, 5, "kg"),
    ("Tere 1", "macarrao", 3.79, 500, "g"),
    ("Tere 1", "macarrao", 4.98, 1, "kg"),
    ("Tere 1", "feijao", 6.99, 1, "kg"),
    ("Tere 1", "acucar", 3.49, 1, "kg"),
    ("Tere 1", "oleo", 7.99, 900, "ml"),
    ("Tere 1", "leite", 4.29, 1, "L"),
    ("Tere 1", "pao", 6.98, 500, "g"),
    ("Dib", "pao", 3.49, 450, "g"),
    ("Armazem", "cafe", 8.99, 500, "g"),
    ("Armazem", "leite_em_po", 11.99, 400, "g"),
    ("Armazem", "leite", 3.99, 1, "L"),
    ("Tere 2", "cafe", 9.98, 500, "g"),
    ("Tere 2", "macarrao", 3.49, 500, "g"),
    ("Tere 2", "macarrao", 4.98, 1, "kg"),
    ("Tere 2", "arroz", 19.98, 5, "kg"),
    ("Tere 2", "feijao", 7.49, 1, "kg"),
    ("Tere 2", "oleo", 7.99, 900, "ml"),
    ("Tere 2", "ovo", 13.98, 30, "unid"),
    ("Tere 2", "amido_de_milho", 3.99, 200, "g"),
    ("Tere 2", "creme_de_arroz", 4.99, 200, "g"),
    ("Tere 2", "farinha_de_aveia", 10.98, 500, "g"),
    ("Tere 2", "cereal", 9.98, 300, "g"),
    ("Tere 2", "adocante", 4.99, 100, "ml"),
    ("Tere 2", "amendoim", 10.98, 500, "g"),
    ("Tere 2", "molho_de_tomate", 1.49, 340, "g"),
    ("Tere 2", "bebida_lactea", 5.99, 900, "ml"),
    ("Xodo", "farinha_de_aveia", 8.98, 500, "g"),
    ("Supermarket", "leite_em_po", 11.98, 400, "g"),
    ("Supermarket", "cereal", 7.49, 300, "g"),
    ("Supermarket", "cereal", 20.98, 730, "g"),
    ("Supermarket", "cafe", 8.98, 500, "g"),
    ("Supermarket", "amido_de_milho", 3.98, 200, "g"),
    ("Supermarket", "amido_de_milho", 11.98, 500, "g"),
    ("Supermarket", "ovo", 9.98, 20, "unid"),
    ("Supermarket", "adocante", 3.98, 100, "ml"),
    ("Supermarket", "pao", 3.59, 450, "g"),
    ("Moises", "cafe", 11.9, 500, "g"),
    ("Moises", "macarrao", 4.99, 1, "kg"),
    ("Moises", "macarrao", 2.99, 500, "g"),
    ("Moises", "amendoim", 8.99, 500, "g"),
    ("Moises", "cereal", 9.99, 300, "g"),
    ("Moises", "oleo", 8.69, 900, "ml"),
    ("Moises", "feijao", 7.49, 1, "kg"),
    ("Moises", "acucar", 3.49, 1, "kg"),
    ("Moises", "adocante", 4.49, 100, "ml"),
)

for register in registers:
    datas.append(load(*register))

with engine.begin() as connection:
    connection.execute(
        market_basket_table.insert(),
        datas
    )
