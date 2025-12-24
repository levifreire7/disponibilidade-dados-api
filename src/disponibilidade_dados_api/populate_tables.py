from sqlalchemy import create_engine, MetaData
from faker import Faker
from hashlib import sha256

metadata = MetaData()

engine = create_engine('postgres://postgres:postgres@localhost:5432/fakedata')

with engine.begin() as conn:
    metadata.reflect(conn)

def insert_data(table_name, n_records):
    faker = Faker('pt_BR')
    if table_name not in metadata.tables.keys():
        raise Exception(f'The {table_name} table does not exist')
    
    with metadata.begin() as conn:
        for _ in range(n_records):
            table = metadata.tables[table_name]
            if table_name == 'customers':
                insert_comand = table.insert.values(
                    cd_customer=sha256(faker.cpf().encode('utf-8')).hexdigest(),
                    nm_customer=faker.name(),
                    st_email=faker.email(),
                    st_phone=faker.phone_number(),
                    st_state=faker.state()[0],
                    dt_bithdate=faker.date_of_birth(minimum_age=18, maximum_age=80)
                )
                conn.execute(insert_comand)


if __name__ == '__main__':
    insert_data(table_name='customers', n_records=1_000_000)