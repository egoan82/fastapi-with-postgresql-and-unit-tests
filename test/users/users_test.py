from faker import Faker
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine

from main import app
from db.database import get_session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


def override_get_db():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_db

fake = Faker()
user_id = None
email = None


def test_list():
    client = TestClient(app)

    response = client.get(
        "/v100/users",
    )

    data = response.json()

    assert response.status_code == 200
    assert data[0]["name"] == "Edward"


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
