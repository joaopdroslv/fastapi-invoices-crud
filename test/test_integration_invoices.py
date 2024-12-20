from invoices.main import app
from shared.dependencies import get_db
from shared.database import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_URL = 'sqlite:///./test/test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
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


def test_list_invoices():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    invoices = [
        {'value': 1000.0, 'paid': False, 'payment_date': None, 'payment_method': None},
        {'value': 2000.0, 'paid': True, 'payment_date': '2024-01-01', 'payment_method': 'credit_card'},
        {'value': 2000.0, 'paid': True, 'payment_date': '2024-01-01', 'payment_method': 'debit_card'},
        {'value': 4000.0, 'paid': True, 'payment_date': '2024-01-01', 'payment_method': 'cash'}
    ]

    for invoice in invoices:
        client.post('/invoices', json=invoice)

    response = client.get('/invoices')

    expected = [
        {'id': 1, 'value': 1000.0, 'paid': False, 'payment_date': None, 'payment_method': None},
        {'id': 2, 'value': 2000.0, 'paid': True, 'payment_date': '2024-01-01', 'payment_method': 'credit_card'},
        {'id': 3, 'value': 2000.0, 'paid': True, 'payment_date': '2024-01-01', 'payment_method': 'debit_card'},
        {'id': 4, 'value': 4000.0, 'paid': True, 'payment_date': '2024-01-01', 'payment_method': 'cash'}
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_list_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {'value': 1000.0, 'paid': False, 'payment_date': None, 'payment_method': None}

    response = client.post('/invoices', json=new_invoice)

    created_invoice_id = response.json()['id']

    response = client.get(f'/invoices/{created_invoice_id}')

    assert response.status_code == 200
    assert response.json() == {'id': 1, 'value': 1000.0, 'paid': False, 'payment_date': None, 'payment_method': None}


def test_list_nonexistent_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.get('/invoices/9999')

    assert response.status_code == 404


def test_create_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {'value': 1000.0, 'paid': False, 'payment_date': None, 'payment_method': None}

    created_invoice = new_invoice.copy()
    created_invoice['id'] = 1

    response = client.post('/invoices', json=new_invoice)

    assert response.status_code == 201
    assert response.json() == created_invoice


def test_create_invoice_with_unkown_payment_method():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {'value': 1000.0, 'paid': True, 'payment_date': '2024-01-01', 'payment_method': 'paypal'}

    created_invoice = new_invoice.copy()
    created_invoice['id'] = 1

    response = client.post('/invoices', json=new_invoice)

    assert response.status_code == 422  # Change this later


def test_not_paid_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {'value': 1000.0, 'paid': False}

    created_invoice = new_invoice.copy()
    created_invoice['id'] = 1
    created_invoice['payment_date'] = None
    created_invoice['payment_method'] = None

    response = client.post('/invoices', json=new_invoice)

    assert response.status_code == 201
    assert response.json() == created_invoice


def test_marking_invoice_as_paid():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {'value': 1000.0, 'paid': False}

    response = client.post('/invoices', json=new_invoice)

    created_invoice_id = response.json()['id']

    updated_invoice = new_invoice.copy()
    updated_invoice['id'] = created_invoice_id
    updated_invoice['paid'] = True
    updated_invoice['payment_date'] = '2024-01-01'
    updated_invoice['payment_method'] = 'credit_card'

    response = client.put(f'/invoices/{created_invoice_id}', json=updated_invoice)

    assert response.status_code == 200


def test_update_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {'value': 1000.0, 'paid': False}

    response = client.post('/invoices', json=new_invoice)

    created_invoice_id = response.json()['id']

    updated_invoice = new_invoice.copy()
    updated_invoice['id'] = created_invoice_id
    updated_invoice['value'] = 2000.0

    response = client.put(f'/invoices/{created_invoice_id}', json=updated_invoice)

    assert response.status_code == 200
    assert response.json()['value'] == 2000.0


def test_update_nonexistent_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.put('/invoices/9999', json={'value': 1000.0, 'paid': False})

    assert response.status_code == 404


def test_delete_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/invoices', json={'value': 1000.0, 'paid': False})

    created_invoice_id = response.json()['id']

    response = client.delete(f'/invoices/{created_invoice_id}')

    assert response.status_code == 204


def test_delete_nonexistent_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.delete('/invoices/9999')

    assert response.status_code == 404
