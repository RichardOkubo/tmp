PRAGMA table_info(market_basket_table)

SELECT * FROM market_basket_table

SELECT market, price, quantity
FROM market_basket_table
WHERE product = 'arroz'
