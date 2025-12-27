from sqlalchemy import create_engine


class DatabaseClient:
    def __init__(self):
        self.database = 'postgresql://postgres:postgres@postgres:5432/fakedata'
        self.engine = create_engine(self.database)
