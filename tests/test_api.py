import os
import requests
import pytest
import uuid

from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('API_BASE_URL') 

@pytest.fixture
def create_user():
    """Создает пользователя для тестирования."""
    user_data = {
        "email": f"test-{uuid.uuid4()}@example.com",
        "password": "password123",
        "name": "Test User"
    }
    response = requests.post(f'{BASE_URL}/register', json=user_data)
    return response.json()

def test_register_user(create_user):
    """Тестирование регистрации нового пользователя."""
    assert create_user['email'] is not None
    assert 'id' in create_user

def test_register_existing_user(create_user):
    """Тестирование регистрации существующего пользователя."""
    response = requests.post(f'{BASE_URL}/register', json=create_user)
    assert response.status_code == 400
    assert response.json()['error'] == 'Пользователь уже существует'

def test_login_user(create_user):
    """Тестирование входа существующего пользователя."""
    login_data = {
        "email": create_user['email'],  
        "password": "password123"
    }
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    assert response.status_code == 200
    assert 'token' in response.json()
    
    return response.json()['token'] 

def test_login_invalid_credentials():
    """Тестирование входа с неверными учетными данными."""
    login_data = {
        "email": "invalid@example.com",
        "password": "wrongpassword"
    }
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    assert response.status_code == 400
    assert response.json()['error'] == 'Неверный логин или пароль'

def test_get_user_by_id(create_user):
    """Тестирование получения пользователя по ID."""
    user_id = create_user['id']
    response = requests.get(f'{BASE_URL}/users/{user_id}')
    assert response.status_code == 200
    assert response.json()['email'] == create_user['email']

def test_update_user(create_user):
    """Тестирование обновления информации о пользователе."""
    user_id = create_user['id']
    

    update_data = {
        "name": "Updated User" 
    }
    
    token = requests.post(f'{BASE_URL}/login', json={
        "email": create_user['email'],
        "password": "password123"
    }).json()['token']
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.put(f'{BASE_URL}/users/{user_id}', json=update_data, headers=headers)
    
    assert response.status_code == 200
    assert response.json()['name'] == update_data['name']  

def test_current_user(create_user):
    """Тестирование получения текущего пользователя."""
    
    token = requests.post(f'{BASE_URL}/login', json={
        "email": create_user['email'],
        "password": "password123"
    }).json()['token']
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f'{BASE_URL}/current', headers=headers)
    
    assert response.status_code == 200
    assert response.json()['email'] == create_user['email']

def test_create_post(create_user):
   """Тестирование создания поста."""
   
   token = requests.post(f'{BASE_URL}/login', json={
       "email": create_user['email'],
       "password": "password123"
   }).json()['token']
   
   headers = {"Authorization": f"Bearer {token}"}
   
   post_data = {
       "content": "This is a test post."
   }
   
   response = requests.post(f'{BASE_URL}/posts', json=post_data, headers=headers)
   
   assert response.status_code == 200
   assert 'id' in response.json()

def test_get_all_posts(create_user):
   """Тестирование получения всех постов."""
   
   token = requests.post(f'{BASE_URL}/login', json={
       "email": create_user['email'],
       "password": "password123"
   }).json()['token']
   
   headers = {"Authorization": f"Bearer {token}"}
   
   response = requests.get(f'{BASE_URL}/posts', headers=headers)
   
   assert response.status_code == 200
   assert isinstance(response.json(), list)

def test_delete_post(create_user):
   """Тестирование удаления поста."""
   
   token = requests.post(f'{BASE_URL}/login', json={
       "email": create_user['email'],
       "password": "password123"
   }).json()['token']
   
   headers = {"Authorization": f"Bearer {token}"}
   
   post_response = requests.post(f'{BASE_URL}/posts', json={"content": "Post to delete"}, headers=headers)
   post_id = post_response.json()['id']
   
   delete_response = requests.delete(f'{BASE_URL}/posts/{post_id}', headers=headers)
   
   assert delete_response.status_code == 200
   assert delete_response.json() is not None

