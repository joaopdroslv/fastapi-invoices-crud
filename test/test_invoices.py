from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.database.dependencies import get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test/test_database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


client = TestClient(app)


# +-------------------------------------------------------------+
# | WARNING                                                     |
# +-------------------------------------------------------------+
# | Some of the tests in this file are outdated and will fail.  |
# | It is necessary to update them to reflect recent changes    |
# | in the API and database schema.                             |
# +-------------------------------------------------------------+


def test_list_invoices():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    invoices = [
        {"value": 1000.0, "paid": False, "payment_date": None, "payment_method": None},
        {
            "value": 2000.0,
            "paid": False,
            "payment_date": None,
            "payment_method": None,
        },
        {
            "value": 3000.0,
            "paid": False,
            "payment_date": None,
            "payment_method": None,
        },
    ]

    for invoice in invoices:
        client.post("/invoices", json=invoice)

    response = client.get("/invoices")

    expected = [
        {
            "id": 1,
            "value": 1000.0,
            "paid": False,
            "payment_date": None,
            "payment_method": None,
            "user": None,
        },
        {
            "id": 2,
            "value": 2000.0,
            "paid": False,
            "payment_date": None,
            "payment_method": None,
            "user": None,
        },
        {
            "id": 3,
            "value": 3000.0,
            "paid": False,
            "payment_date": None,
            "payment_method": None,
            "user": None,
        },
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_list_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {
        "value": 1000.0,
        "paid": False,
        "payment_date": None,
        "payment_method": None,
    }

    response = client.post("/invoices", json=new_invoice)

    created_invoice_id = response.json()["id"]

    created_invoice = new_invoice.copy()
    created_invoice["id"] = created_invoice_id
    created_invoice["user"] = None

    response = client.get(f"/invoices/{created_invoice_id}")

    assert response.status_code == 200
    assert response.json() == created_invoice


def test_list_user_invoices():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Creates a new user
    new_user = {"first_name": "Michael", "last_name": "Smith"}

    response = client.post("/users", json=new_user)

    created_user_id = response.json()["id"]

    invoices = [
        {
            "value": 1000.0,
            "paid": False,
            "payment_date": None,
            "payment_method": None,
            "user_id": created_user_id,
        },
        {
            "value": 2000.0,
            "paid": False,
            "payment_date": None,
            "payment_method": None,
            "user_id": created_user_id,
        },
        {
            "value": 3000.0,
            "paid": False,
            "payment_date": None,
            "payment_method": None,
            "user_id": created_user_id,
        },
    ]

    for invoice in invoices:
        client.post("/invoices", json=invoice)

    response = client.get(f"/users/{created_user_id}/invoices")

    assert response.status_code == 200
    assert len(response.json()) == 3


def test_list_user_invoices_to_an_user_with_no_invoices():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Creates a new user
    new_user = {"first_name": "Michael", "last_name": "Smith"}

    response = client.post("/users", json=new_user)

    created_user_id = response.json()["id"]

    response = client.get(f"/users/{created_user_id}/invoices")

    assert response.status_code == 200
    assert response.json() == []


def test_list_nonexistent_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.get("/invoices/9999")

    assert response.status_code == 404


def test_create_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {
        "value": 1000.0,
        "paid": False,
        "payment_date": None,
        "payment_method": None,
    }

    created_invoice = new_invoice.copy()
    created_invoice["id"] = 1
    created_invoice["user"] = None

    response = client.post("/invoices", json=new_invoice)

    assert response.status_code == 201
    assert response.json() == created_invoice


def test_create_invoice_to_an_especific_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Creates a new user
    new_user = {"first_name": "Michael", "last_name": "Smith"}

    response = client.post("/users", json=new_user)

    created_user_id = response.json()["id"]

    created_user = new_user.copy()
    created_user["id"] = created_user_id

    # Creates a new invoice
    new_invoice = {
        "value": 1000.0,
        "paid": False,
        "payment_date": None,
        "payment_method": None,
        "user_id": created_user_id,
    }

    response = client.post("/invoices", json=new_invoice)

    del new_invoice["user_id"]  # Only necessary to create the invoice

    created_invoice_id = response.json()["id"]

    created_invoice = new_invoice.copy()
    created_invoice["id"] = created_invoice_id
    created_invoice["user"] = created_user

    assert response.status_code == 201
    assert response.json() == created_invoice


def test_create_invoice_to_a_nonexistent_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {
        "value": 1000.0,
        "paid": False,
        "payment_date": None,
        "payment_method": None,
        "user_id": 9999,
    }

    response = client.post("/invoices", json=new_invoice)

    assert response.status_code == 404


def test_create_invoice_with_unkown_payment_method():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {
        "value": 1000.0,
        "paid": True,
        "payment_date": "2024-01-01",
        "payment_method": "paypal",
    }

    created_invoice = new_invoice.copy()
    created_invoice["id"] = 1

    response = client.post("/invoices", json=new_invoice)

    assert response.status_code == 422  # Create an error handler for this


def test_create_not_paid_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {"value": 1000.0, "paid": False}

    created_invoice = new_invoice.copy()
    created_invoice["id"] = 1
    created_invoice["payment_date"] = None
    created_invoice["payment_method"] = None
    created_invoice["user"] = None

    response = client.post("/invoices", json=new_invoice)

    assert response.status_code == 201
    assert response.json() == created_invoice


def test_marking_invoice_as_paid():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {"value": 1000.0, "paid": False}

    response = client.post("/invoices", json=new_invoice)

    created_invoice_id = response.json()["id"]

    updated_invoice = new_invoice.copy()
    updated_invoice["id"] = created_invoice_id
    updated_invoice["paid"] = True
    updated_invoice["payment_date"] = "2024-01-01"
    updated_invoice["payment_method"] = "credit_card"

    response = client.put(f"/invoices/{created_invoice_id}", json=updated_invoice)

    assert response.status_code == 200


def test_update_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {"value": 1000.0, "paid": False}

    response = client.post("/invoices", json=new_invoice)

    created_invoice_id = response.json()["id"]

    updated_invoice = new_invoice.copy()
    updated_invoice["id"] = created_invoice_id
    updated_invoice["value"] = 10000.0

    response = client.put(f"/invoices/{created_invoice_id}", json=updated_invoice)

    assert response.status_code == 200
    assert response.json()["value"] == 10000.0


def test_update_nonexistent_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.put("/invoices/9999", json={"value": 1000.0, "paid": False})

    assert response.status_code == 404


def test_link_invoice_to_an_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Creates a new user
    new_user = {"first_name": "Michael", "last_name": "Smith"}

    response = client.post("/users", json=new_user)

    created_user_id = response.json()["id"]

    created_user = new_user.copy()
    created_user["id"] = created_user_id

    # Creates a new invoice
    new_invoice = {"value": 1000.0, "paid": False}

    response = client.post("/invoices", json=new_invoice)

    created_invoice_id = response.json()["id"]

    updated_invoice = new_invoice.copy()
    updated_invoice["id"] = created_invoice_id
    updated_invoice["payment_date"] = None
    updated_invoice["payment_method"] = None
    updated_invoice["user_id"] = created_user_id

    response = client.put(f"/invoices/{created_invoice_id}", json=updated_invoice)

    del updated_invoice["user_id"]
    updated_invoice["user"] = created_user

    assert response.status_code == 200
    assert response.json() == updated_invoice


def test_link_an_already_linked_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Creates two new users
    first_new_user = {
        "first_name": "Michael",
        "last_name": "Smith",
    }  # The invoice will be linked to this user at first
    second_new_user = {"first_name": "Walter", "last_name": "Scott"}

    first_response = client.post("/users", json=first_new_user)
    second_response = client.post("/users", json=second_new_user)

    first_created_user_id = first_response.json()["id"]
    second_created_user_id = second_response.json()["id"]

    created_user = first_new_user.copy()
    created_user["id"] = first_created_user_id

    # Creates a new invoice
    new_invoice = {"value": 1000.0, "paid": False, "user_id": first_created_user_id}

    response = client.post("/invoices", json=new_invoice)

    created_invoice_id = response.json()["id"]

    updated_invoice = new_invoice.copy()
    updated_invoice["user_id"] = second_created_user_id

    response = client.put(f"/invoices/{created_invoice_id}", json=updated_invoice)

    assert response.status_code == 422


def test_link_invoice_to_a_nonexistent_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {"value": 1000.0, "paid": False}

    response = client.post("/invoices", json=new_invoice)

    created_invoice_id = response.json()["id"]

    updated_invoice = new_invoice.copy()
    updated_invoice["id"] = created_invoice_id
    updated_invoice["user_id"] = 9999

    response = client.put(f"/invoices/{created_invoice_id}", json=updated_invoice)

    assert response.status_code == 404


def test_delete_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/invoices", json={"value": 1000.0, "paid": False})

    created_invoice_id = response.json()["id"]

    response = client.delete(f"/invoices/{created_invoice_id}")

    assert response.status_code == 204


def test_delete_nonexistent_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.delete("/invoices/9999")

    assert response.status_code == 404
