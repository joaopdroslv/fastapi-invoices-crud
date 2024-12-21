from src.main import app
from src.database.dependencies import get_db
from src.database.database import Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient


SQLALCHEMY_DATABASE_URL = 'sqlite:///./test/test_database.db'

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


def test_list_users():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    users = [
        {'first_name': 'Michael', 'last_name': 'Smith'},
        {'first_name': 'Walter', 'last_name': 'Scott'},
        {'first_name': 'Roland', 'last_name': 'Weeks'},
        {'first_name': 'Alex', 'last_name': 'Jackson'},
        {'first_name': 'James', 'last_name': 'Roberts'}
    ]

    for user in users:
        client.post('/users', json=user)

    response = client.get('/users')

    expected = [
        {'id': 1, 'first_name': 'Michael', 'last_name': 'Smith'},
        {'id': 2, 'first_name': 'Walter', 'last_name': 'Scott'},
        {'id': 3, 'first_name': 'Roland', 'last_name': 'Weeks'},
        {'id': 4, 'first_name': 'Alex', 'last_name': 'Jackson'},
        {'id': 5, 'first_name': 'James', 'last_name': 'Roberts'}
    ]

    assert response.status_code == 200
    assert response.json() == expected


def test_list_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_user = {'first_name': 'Michael', 'last_name': 'Smith'}

    response = client.post('/users', json=new_user)

    created_user_id = response.json()['id']

    created_user = new_user.copy()
    created_user['id'] = 1

    response = client.get(f'/users/{created_user_id}')

    assert response.status_code == 200
    assert response.json() == created_user


def test_list_nonexistent_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.get('/users/9999')

    assert response.status_code == 404


def test_create_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_user = {'first_name': 'Michael', 'last_name': 'Smith'}

    created_user = new_user.copy()
    created_user['id'] = 1

    response = client.post('/users', json=new_user)

    assert response.status_code == 201
    assert response.json() == created_user


def test_update_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_user = {'first_name': 'Michael', 'last_name': 'Smith'}

    response = client.post('/users', json=new_user)

    created_user_id = response.json()['id']

    updated_user = new_user.copy()
    updated_user['id'] = 1
    updated_user['first_name'] = 'Walter'
    updated_user['last_name'] = 'Scott'

    response = client.put(f'/users/{created_user_id}', json=updated_user)

    assert response.status_code == 200
    assert response.json() == updated_user


def test_update_nonexistent_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.put('/users/9999', json={'first_name': 'Michael', 'last_name': 'Smith'})

    assert response.status_code == 404


def test_delete_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/users', json={'first_name': 'Michael', 'last_name': 'Smith'})

    created_user_id = response.json()['id']

    response = client.delete(f'/users/{created_user_id}')

    assert response.status_code == 204


def test_delete_nonexistent_user():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.delete('/users/9999')

    assert response.status_code == 404
