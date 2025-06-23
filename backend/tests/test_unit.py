import pytest
from db.ops import SQLAlchemyOps

def test_create_table():
    db_ops = SQLAlchemyOps()
    db_ops.create_table('test_table', ['id', 'name', 'value'])
    result = db_ops.fetch_data('test_table')
    assert result == []
    db_ops.close_connection()
