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

    client.post('/invoices', json={'value': 3456.1, 'paid': False, 'payment_date': None, 'payment_method': None})
    client.post('/invoices', json={'value': 1099.99, 'paid': True, 'payment_date': '2024-11-15', 'payment_method': 'debit_card'})
    client.post('/invoices', json={'value': 257.89, 'paid': True, 'payment_date': '2024-11-20', 'payment_method': 'credit_card'})

    response = client.get('/invoices')

    assert response.status_code == 200
    assert response.json() == [
        {'id': 1, 'value': 3456.1, 'paid': False, 'payment_date': None, 'payment_method': None}, 
        {'id': 2, 'value': 1099.99, 'paid': True, 'payment_date': '2024-11-15', 'payment_method': 'debit_card'}, 
        {'id': 3, 'value': 257.89, 'paid': True, 'payment_date': '2024-11-20', 'payment_method': 'credit_card'}
    ]


def test_list_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/invoices', json={'value': 3456.1, 'paid': False, 'payment_date': None, 'payment_method': None})

    created_invoice_id = response.json()['id']

    response = client.get(f'/invoices/{created_invoice_id}')

    assert response.status_code == 200
    assert response.json() == {'id': 1, 'value': 3456.1, 'paid': False, 'payment_date': None, 'payment_method': None}


def test_create_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {
        'value': 1199.99,
        'paid': False,
        'payment_date': None,
        'payment_method': None,
    }

    new_invoice_copy = new_invoice.copy()
    new_invoice_copy['id'] = 1

    response = client.post('/invoices', json=new_invoice)

    assert response.status_code == 201
    assert response.json() == new_invoice_copy


def test_not_paid_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_invoice = {
        'value': 1199.99,
        'paid': False,
    }

    new_invoice_copy = new_invoice.copy()
    new_invoice_copy['id'] = 1
    new_invoice_copy['payment_date'] = None
    new_invoice_copy['payment_method'] = None

    response = client.post('/invoices', json=new_invoice)

    assert response.status_code == 201
    assert response.json() == new_invoice_copy


def test_marking_invoice_as_paid():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/invoices', json={
        'value': 1000.0,
        'paid': False,
    })

    created_invoice_id = response.json()['id']

    response = client.put(f'/invoices/{created_invoice_id}', json={
        'value': 1000.0,
        'paid': True,
        'payment_date': '2024-01-01',
        'payment_method': 'credit_card'
    })

    assert response.status_code == 200


def test_update_invoice_value():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/invoices', json={
        'value': 1000.0,
        'paid': False,
    })

    created_invoice_id = response.json()['id']

    NEW_VALUE = 2000.0

    response = client.put(f'/invoices/{created_invoice_id}', json={
        'value': NEW_VALUE,
        'paid': False,
    })

    assert response.status_code == 200
    assert response.json()['value'] == NEW_VALUE


def test_delete_invoice():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/invoices', json={
        'value': 1000.0,
        'paid': False,
    })

    created_invoice_id = response.json()['id']

    response = client.delete(f'/invoices/{created_invoice_id}')

    assert response.status_code == 204
