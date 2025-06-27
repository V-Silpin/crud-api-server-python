"""
Test database operations and connection handling.
"""
import pytest
import os
from unittest.mock import patch
from db.ops import PostgresOps


def test_database_connection_with_url():
    """Test database connection using DATABASE_URL."""
    # Test with a valid URL format
    test_url = "postgresql://user:pass@localhost:5432/testdb"
    
    with patch('db.ops.create_engine') as mock_create_engine:
        db = PostgresOps(database_url=test_url)
        mock_create_engine.assert_called_once_with(test_url)


def test_database_connection_with_env_vars():
    """Test database connection using environment variables."""
    test_env = {
        'DB_NAME': 'testdb',
        'DB_HOST': 'localhost',
        'DB_USER': 'testuser',
        'DB_PASS': 'testpass',
        'DB_PORT': '5432'
    }
    
    with patch.dict(os.environ, test_env), \
         patch('db.ops.create_engine') as mock_create_engine:
        
        db = PostgresOps()
        expected_url = "postgresql+psycopg2://testuser:testpass@localhost:5432/testdb"
        mock_create_engine.assert_called_once_with(expected_url)


def test_missing_environment_variables():
    """Test error handling when environment variables are missing."""
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(ValueError) as exc_info:
            PostgresOps()
        
        assert "Missing required environment variables" in str(exc_info.value)


def test_invalid_port():
    """Test error handling when port is not a valid integer."""
    test_env = {
        'DB_NAME': 'testdb',
        'DB_HOST': 'localhost',
        'DB_USER': 'testuser',
        'DB_PASS': 'testpass',
        'DB_PORT': 'invalid_port'
    }
    
    with patch.dict(os.environ, test_env):
        with pytest.raises(ValueError) as exc_info:
            PostgresOps()
        
        assert "DB_PORT must be a valid integer" in str(exc_info.value)


def test_default_values():
    """Test that default values are used when environment variables are empty strings."""
    test_env = {
        'DB_NAME': '',
        'DB_HOST': '',
        'DB_USER': '',
        'DB_PASS': '',
        'DB_PORT': ''
    }
    
    with patch.dict(os.environ, test_env), \
         patch('db.ops.create_engine') as mock_create_engine:
        
        db = PostgresOps()
        expected_url = "postgresql+psycopg2://postgres:postgres@localhost:5432/postgres"
        mock_create_engine.assert_called_once_with(expected_url)


def test_database_url_takes_precedence():
    """Test that DATABASE_URL takes precedence over individual env vars."""
    test_env = {
        'DATABASE_URL': 'postgresql://override:pass@override:1234/override',
        'DB_NAME': 'ignored',
        'DB_HOST': 'ignored',
        'DB_USER': 'ignored',
        'DB_PASS': 'ignored',
        'DB_PORT': 'ignored'
    }
    
    with patch.dict(os.environ, test_env), \
         patch('db.ops.create_engine') as mock_create_engine:
        
        # Simulate how it's used in routes.py
        database_url = os.getenv("DATABASE_URL")
        db = PostgresOps(database_url=database_url)
        
        mock_create_engine.assert_called_once_with('postgresql://override:pass@override:1234/override')


def test_connection_error_handling():
    """Test error handling when database connection fails."""
    with patch('db.ops.create_engine') as mock_create_engine:
        mock_create_engine.side_effect = Exception("Connection failed")
        
        with pytest.raises(ConnectionError) as exc_info:
            PostgresOps(database_url="postgresql://user:pass@localhost:5432/testdb")
        
        assert "Failed to connect to database" in str(exc_info.value)


@pytest.mark.integration
def test_real_database_operations():
    """Integration test with real database (requires DATABASE_URL)."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL not set, skipping integration test")
    
    try:
        db = PostgresOps(database_url=database_url)
        
        # Test table creation
        db.create_table("test_items", ["id", "name", "description", "price"])
        
        # Test data insertion
        db.insert_data("test_items", [1, "Test Course", "Test Description", 99.99])
        
        # Test data retrieval
        data = db.fetch_data("test_items")
        assert len(data) > 0
        assert data[0]["name"] == "Test Course"
        
        # Test data update
        db.update_data("test_items", {"price": 149.99}, {"id": 1})
        updated_data = db.fetch_data("test_items")
        assert updated_data[0]["price"] == 149.99
        
        # Test data deletion
        db.delete_data("test_items", {"id": 1})
        final_data = db.fetch_data("test_items")
        assert len(final_data) == 0
        
    except Exception as e:
        pytest.fail(f"Integration test failed: {e}")
    finally:
        if 'db' in locals():
            db.close_connection()
