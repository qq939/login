import pytest
import zlib
from models import db, app, create_user, get_user_by_username, user_models, SHARD_COUNT

def get_shard_index(username):
    return zlib.crc32(username.encode('utf-8')) % SHARD_COUNT

def test_user_sharding_by_username():
    """
    Test that users are saved to the correct shard based on Username.
    """
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        # Find two usernames that map to different shards
        # This is a bit brute force to find them, or we calculate.
        # SHARD_COUNT is 2.
        
        # "alice" -> ?
        u1 = "alice"
        shard1 = get_shard_index(u1)
        
        # "bob" -> ?
        u2 = "bob"
        shard2 = get_shard_index(u2)
        
        # If they are same, try another
        if shard1 == shard2:
            u2 = "charlie"
            shard2 = get_shard_index(u2)
            
        assert shard1 != shard2
        
        # Create users
        create_user(u1, "pass1")
        create_user(u2, "pass2")
        
        # Verify u1 is in shard1
        User1 = user_models[shard1]
        user_db1 = db.session.execute(db.select(User1).filter_by(username=u1)).scalar_one_or_none()
        assert user_db1 is not None
        assert user_db1.username == u1
        
        # Verify u1 is NOT in shard2
        User2 = user_models[shard2]
        user_db_not = db.session.execute(db.select(User2).filter_by(username=u1)).scalar_one_or_none()
        assert user_db_not is None
        
        # Verify u2 is in shard2
        user_db2 = db.session.execute(db.select(User2).filter_by(username=u2)).scalar_one_or_none()
        assert user_db2 is not None

def test_get_user():
    with app.app_context():
        db.create_all()
        username = "testuser"
        create_user(username, "pass")
        
        user = get_user_by_username(username)
        assert user is not None
        assert user.username == username
