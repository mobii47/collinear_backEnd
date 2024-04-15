from fastapi.testclient import TestClient
from your_main_module import (
    app,
)  # Replace "your_main_module" with the name of your main FastAPI module
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from your_database_module import (
    Base,
)  # Replace "your_database_module" with the name of your database module
from your_models_module import (
    User,
)  # Replace "your_models_module" with the name of your models module

# Set up testing database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override dependency to use testing database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Initialize test client
client = TestClient(app)

# Define test cases


def test_register_user():
    # Test valid registration
    response = client.post(
        "/register/", json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

    # Test registration with existing email
    response = client.post(
        "/register/", json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert "Email already exists" in response.text


def test_get_user():
    # Test valid user retrieval
    user_id = 1  # Assuming there is a user with ID 1 in the database
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

    # Test user retrieval with non-existent ID
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "User not found" in response.text


def test_login_user():
    # Test valid login
    response = client.post(
        "/login/", json={"email": "test@example.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Test login with invalid email
    response = client.post(
        "/login/", json={"email": "nonexistent@example.com", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert "Invalid email" in response.text

    # Test login with invalid password
    response = client.post(
        "/login/", json={"email": "test@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 400
    assert "Invalid password" in response.text
