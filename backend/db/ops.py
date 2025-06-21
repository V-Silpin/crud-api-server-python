from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, select, and_, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

class SQLAlchemyOps:
    def __init__(self):
        load_dotenv()
        database = os.getenv("DB_NAME")
        host = os.getenv("DB_HOST")
        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASS")
        port = os.getenv("DB_PORT")
        url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        self.engine = create_engine(url)
        self.metadata = MetaData()
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_table(self, table_name, columns):
        table = Table(
            table_name, self.metadata,
            Column('id', Integer),
            *(Column(col, String) for col in columns if col != 'id'),
            extend_existing=True
        )
        table.drop(self.engine, checkfirst=True)
        table.create(self.engine, checkfirst=True)

    def insert_data(self, table_name, data):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        ins = table.insert().values(dict(zip(table.columns.keys(), data)))
        with self.engine.begin() as conn:
            conn.execute(ins)

    def fetch_data(self, table_name):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        stmt = select(table)
        with self.engine.connect() as conn:
            result = conn.execute(stmt)
            return [dict(row._mapping) for row in result]

    def update_data(self, table_name, set_values, condition):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        stmt = table.update().where(
            and_(*(getattr(table.c, k) == v for k, v in condition.items()))
        ).values(**set_values)
        with self.engine.begin() as conn:
            conn.execute(stmt)

    def delete_data(self, table_name, condition):
        table = Table(table_name, self.metadata, autoload_with=self.engine)
        stmt = table.delete().where(
            and_(*(getattr(table.c, k) == v for k, v in condition.items()))
        )
        with self.engine.begin() as conn:
            conn.execute(stmt)

    def close_connection(self):
        self.session.close()
        self.engine.dispose()

PostgresOps = SQLAlchemyOps