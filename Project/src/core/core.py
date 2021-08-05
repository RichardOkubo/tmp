from sqlalchemy import (create_engine, MetaData, Column,
                        Table, Integer, String, Float)

DB_URL = 'sqlite:///../../data/database.db'
engine = create_engine(DB_URL)

metadata = MetaData(bind=engine)

products_table = Table(
    'products_table', metadata,
    Column('id', Integer, primary_key=True),
    Column('product', String(50), nullable=False),
    Column('price', Float, nullable=False),
    Column('quantity', String(25), nullable=False))

metadata.create_all()
