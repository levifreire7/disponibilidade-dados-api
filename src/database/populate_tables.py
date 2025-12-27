import random

from sqlalchemy import create_engine, MetaData
from faker import Faker
import faker_commerce
from hashlib import sha256

metadata = MetaData()

engine = create_engine('postgresql://postgres:postgres@localhost:5432/fakedata')

with engine.begin() as conn:
    metadata.reflect(conn)

def insert_customers_data(table_name, n_records):
    faker = Faker('pt_BR')
    if table_name not in metadata.tables.keys():
        raise Exception(f'The {table_name} table does not exist')
    
    customers_codes = []
    with engine.begin() as conn:
        for _ in range(n_records):
            table = metadata.tables[table_name]
            if table_name == 'customers':
                cd_customer = sha256(faker.unique.cpf().encode('utf-8')).hexdigest()
                customers_codes.append(cd_customer)
                insert_comand = table.insert().values(
                    cd_customer=cd_customer,
                    nm_customer=faker.name(),
                    st_email=faker.email(),
                    st_phone=faker.phone_number(),
                    sg_state=faker.state_abbr(),
                    dt_birth=faker.date_of_birth(minimum_age=18, maximum_age=80)
                )
                conn.execute(insert_comand)
    return customers_codes


def insert_sales_data(table_name, n_records, customers_codes):
    faker = Faker('pt_BR')
    faker.add_provider(faker_commerce.Provider)

    if table_name not in metadata.tables.keys():
        raise Exception(f'The {table_name} table does not exist')
    
    with engine.begin() as conn:
        for _ in range(n_records):
            table = metadata.tables[table_name]
            if table_name == 'sales':
                num_items=random.randint(1, 10)
                price=round(random.uniform(10.00, 1000.00), 2)
                total_value = num_items * price
                insert_command = table.insert().values(
                    cd_customer=random.choice(customers_codes),
                    dt_purchase_date=faker.date_this_year(),
                    product_name=faker.ecommerce_name(),
                    num_items=num_items,
                    price=price,
                    shipping_cost=round(random.uniform(10.00, 100.00), 2),
                    total_value=total_value
                )
                conn.execute(insert_command)


if __name__ == '__main__':
    customers_codes = insert_customers_data(table_name='customers', n_records=1_000)
    insert_sales_data(table_name='sales', n_records=1_500, customers_codes=customers_codes)
    print('All the data has been entered.')