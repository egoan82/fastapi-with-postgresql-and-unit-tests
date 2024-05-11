import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel

from main import app
from db.database import get_session

from db.tables.users import User

# sqlite_file_name = "./database_test.db"
# sqlite_url = f"sqlite:///{sqlite_file_name}"
# engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"
engine = create_engine(DATABASE_URL)


def override_get_db():
    session_engine: Session = Session(engine)
    try:
        with session_engine as session:
            yield session
    except Exception as e:
        pytest.exit(f"Database connection error: {e.args[0]}")
    finally:
        session_engine.close()


SQLModel.metadata.create_all(engine)

app.dependency_overrides[get_session] = override_get_db

fake = Faker(locale="es_CO")
user_id = None
email = None


def test_create_error():
    global user_id, email
    client = TestClient(app)

    data = {
        "name": fake.first_name(),
        "first_last_name": fake.last_name(),
        "second_last_name": 12345,
        "email": "correo@correo",
    }

    response = client.post(
        "/v100/users",
        json=data
    )

    data = response.json()
    print(f"\nnew user: {data}")

    assert response.status_code == 422


def test_create():
    global user_id, email
    client = TestClient(app)

    data = {
        "name": fake.first_name(),
        "first_last_name": fake.last_name(),
        "second_last_name": fake.last_name(),
        "email": fake.email(),
    }

    response = client.post(
        "/v100/users",
        json=data
    )

    data = response.json()
    print(f"\nnew user: {data}")

    assert response.status_code == 201
    user_id = data["id"]
    email = data["email"]


def test_list():
    global user_id, email
    client = TestClient(app)

    response = client.get(
        "/v100/users",
    )

    data = response.json()
    print(f"list users: {data}")

    assert response.status_code == 200


def test_get_one():
    global user_id, email
    client = TestClient(app)

    response = client.get(
        f"/v100/users/{user_id}",
    )

    data = response.json()
    print(f"get user: {data}")

    assert response.status_code == 200
    assert data["id"] == user_id
    assert data["email"] == email


def test_update():
    global user_id, email
    client = TestClient(app)

    data = {
        "name": fake.first_name(),
        "first_last_name": fake.last_name(),
        "second_last_name": fake.last_name(),
        "email": fake.email(),
    }

    response = client.put(
        f"/v100/users/{user_id}",
        json=data
    )

    data = response.json()
    print(f"update user: {data}")

    assert response.status_code == 200
    assert data["id"] == user_id


def test_get_one_update():
    global user_id, email
    client = TestClient(app)

    response = client.get(
        f"/v100/users/{user_id}",
    )

    data = response.json()
    print(f"get user update: {data}")

    assert response.status_code == 200
    assert data["id"] == user_id


def test_delete():
    global user_id
    client = TestClient(app)

    response = client.delete(
        f"/v100/users/{user_id}",
    )

    data = response.content
    print(f"delete user: {data}")

    assert response.status_code == 204
    assert data == b''
