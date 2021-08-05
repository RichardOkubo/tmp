from sqlalchemy.engine import create_engine
from sqlalchemy.sql.schema import Column, MetaData, Table
from sqlalchemy.sql.sqltypes import Float, Integer, String 

DB_URL = 'sqlite:///../../data/market_basket.db'

engine = create_engine(DB_URL)
metadata = MetaData(bind=engine)

market_basket_table = Table(
    "market_basket_table", metadata,
    Column("id", Integer, primary_key=True),
    Column("market", String, nullable=False),
    Column("product", String, nullable=False),
    Column("price", Float, nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("measurement", String, nullable=False)
)

metadata.create_all()
