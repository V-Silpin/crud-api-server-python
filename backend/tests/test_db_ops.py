import pytest
from db.ops import SQLAlchemyOps

@pytest.fixture(scope="function")
def db_ops():
    db = SQLAlchemyOps()
    db.create_table('test_table', ['id', 'name', 'value'])
    yield db
    db.close_connection()

def test_insert_and_fetch_data(db_ops):
    db_ops.insert_data('test_table', [1, 'foo', 'bar'])
    result = db_ops.fetch_data('test_table')
    assert len(result) == 1
    assert result[0]['id'] == 1
    assert result[0]['name'] == 'foo'
    assert result[0]['value'] == 'bar'

def test_update_data(db_ops):
    db_ops.insert_data('test_table', [2, 'baz', 'qux'])
    db_ops.update_data('test_table', {'name': 'updated'}, {'id': 2})
    result = db_ops.fetch_data('test_table')
    assert result[0]['name'] == 'updated'

def test_delete_data(db_ops):
    db_ops.insert_data('test_table', [3, 'del', 'me'])
    db_ops.delete_data('test_table', {'id': 3})
    result = db_ops.fetch_data('test_table')
    assert result == []
