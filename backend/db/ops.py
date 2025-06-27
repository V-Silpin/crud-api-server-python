from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer, select, and_, text
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

class SQLAlchemyOps:
    def __init__(self, database_url=None):
        load_dotenv()
        
        if database_url:
            # Use provided database URL (useful for testing)
            url = database_url
        else:
            # Build URL from environment variables with defaults
            database = os.getenv("DB_NAME", "postgres")
            host = os.getenv("DB_HOST", "localhost")
            user = os.getenv("DB_USER", "postgres")
            password = os.getenv("DB_PASS", "postgres")
            port = os.getenv("DB_PORT", "5432")
            
            # Validate environment variables
            if not all([database, host, user, password, port]):
                missing_vars = []
                if not database: missing_vars.append("DB_NAME")
                if not host: missing_vars.append("DB_HOST")
                if not user: missing_vars.append("DB_USER")
                if not password: missing_vars.append("DB_PASS")
                if not port: missing_vars.append("DB_PORT")
                
                raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
            
            # Validate port is numeric
            try:
                port = int(port)
            except ValueError:
                raise ValueError(f"DB_PORT must be a valid integer, got: {port}")
            
            url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
        
        try:
            self.engine = create_engine(url)
            self.metadata = MetaData()
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
        except Exception as e:
            raise ConnectionError(f"Failed to connect to database: {e}")

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