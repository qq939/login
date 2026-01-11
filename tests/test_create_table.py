import os
import pytest
from sqlalchemy import inspect
from models import db, SHARD_COUNT, app
import createTable

def test_create_tables():
    """
    Test that the create_tables function correctly creates the sharded user tables.
    """
    # Configure app for testing to use in-memory database or a separate test db file
    # But for this simple script, we might just test the side effect on the configured DB.
    # To be safe and clean, let's use a temporary file or in-memory.
    
    with app.app_context():
        # Drop all tables first to ensure clean state
        db.drop_all()
        
        # Run the creation logic
        createTable.create_tables()
        
        # Inspect database
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        print(f"Created tables: {tables}")
        
        # Verify all shard tables exist
        for i in range(SHARD_COUNT):
            table_name = f'user_{i}'
            assert table_name in tables, f"Table {table_name} was not created"
