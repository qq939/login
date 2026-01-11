import pytest
from app import app as flask_app
from models import db, create_user

@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    # Use in-memory db for speed if possible, but we are using sqlite:///users.db in models.py
    # We can override it here
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with flask_app.test_client() as client:
        with flask_app.app_context():
            db.drop_all()
            db.create_all()
        yield client
        with flask_app.app_context():
            db.drop_all()

def test_login_page_get(client):
    """Test that the login page loads."""
    response = client.get('/login')
    assert response.status_code == 200
    # We expect a form
    assert b'<form' in response.data

def test_login_success(client):
    """Test valid login."""
    with flask_app.app_context():
        create_user("validuser", "secret")
        
    response = client.post('/login', data={
        'username': 'validuser', 
        'password': 'secret'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b"Login successful" in response.data

def test_login_fail_wrong_password(client):
    """Test invalid password."""
    with flask_app.app_context():
        create_user("validuser", "secret")
        
    response = client.post('/login', data={
        'username': 'validuser', 
        'password': 'wrongpassword'
    }, follow_redirects=True)
    
    assert b"Login successful" not in response.data
    assert b"Invalid credentials" in response.data or b"Login" in response.data

def test_login_fail_unknown_user(client):
    """Test unknown user."""
    response = client.post('/login', data={
        'username': 'unknown', 
        'password': 'any'
    }, follow_redirects=True)
    
    assert b"Login successful" not in response.data
