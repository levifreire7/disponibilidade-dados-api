from sqlalchemy import create_engine, MetaData, Table, Column, String, Date, Integer, Numeric, ForeignKey

engine = create_engine('postgresql://postgres:postgres@localhost:5432/fakedata')

metadata = MetaData()

customers_table = Table(
    'customers',
    metadata,
    Column('cd_customer', String(256), primary_key=True),
    Column('nm_customer', String(135), nullable=False),
    Column('st_email', String(135), nullable=False),
    Column('st_phone', String(135), nullable=False),
    Column('sg_state', String(2), nullable=False),
    Column('dt_birth', Date, nullable=False)
)

sales_table = Table(
    'sales',
    metadata,
    Column('cd_sale', Integer, primary_key=True, autoincrement=True),
    Column('cd_customer', String(256), ForeignKey('customers.cd_customer')),
    Column('dt_purchase_date', Date, nullable=False),
    Column('product_name', String(135), nullable=False),
    Column('num_items', Integer, nullable=False),
    Column('price', Numeric(18, 2), nullable=False),
    Column('shipping_cost', Numeric(18, 2), nullable=False),
    Column('total_value', Numeric(18, 2), nullable=False)

)

with engine.begin() as conn:
    metadata.create_all(conn)
    for table in metadata.tables.keys():
        print(f'{table} successfully created!')