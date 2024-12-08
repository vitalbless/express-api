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
    print(f"Register user response status code: {response.status_code}")  # Выводим статус-код
    assert response.status_code == 200  # Проверяем успешную регистрацию
    return response.json()

def get_auth_token(email, password):
    """Получает токен для аутентификации."""
    login_data = {
        "email": email,
        "password": password
    }
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    print(f"Login response status code: {response.status_code}")  # Выводим статус-код
    assert response.status_code == 200  # Проверяем успешный вход
    return response.json()['token']

def test_register_user(create_user):
    """Тестирование регистрации нового пользователя."""
    assert create_user['email'] is not None
    assert 'id' in create_user

def test_register_existing_user(create_user):
    """Тестирование регистрации существующего пользователя."""
    response = requests.post(f'{BASE_URL}/register', json=create_user)
    print(f"Register existing user response status code: {response.status_code}")  # Выводим статус-код
    assert response.status_code == 400
    assert response.json()['error'] == 'Пользователь уже существует'

def test_login_user(create_user):
    """Тестирование входа существующего пользователя."""
    token = get_auth_token(create_user['email'], "password123")
    assert token is not None

def test_login_invalid_credentials():
    """Тестирование входа с неверными учетными данными."""
    login_data = {
        "email": "invalid@example.com",
        "password": "wrongpassword"
    }
    response = requests.post(f'{BASE_URL}/login', json=login_data)
    print(f"Login invalid credentials response status code: {response.status_code}")  # Выводим статус-код
    assert response.status_code == 400
    assert response.json()['error'] == 'Неверный логин или пароль'

def test_get_user_by_id(create_user):
    """Тестирование получения пользователя по ID."""
    user_id = create_user['id']
    
    token = get_auth_token(create_user['email'], "password123")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f'{BASE_URL}/users/{user_id}', headers=headers)
    
    print(f"Get user by ID response status code: {response.status_code}")  # Выводим статус-код
    assert response.status_code == 200
    assert response.json()['email'] == create_user['email']

def test_update_user(create_user):
    """Тестирование обновления информации о пользователе."""
    user_id = create_user['id']
    
    update_data = {
        "name": "Updated User"
    }
    
    token = get_auth_token(create_user['email'], "password123")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.put(f'{BASE_URL}/users/{user_id}', json=update_data, headers=headers)
    
    print(f"Update user response status code: {response.status_code}")  # Выводим статус-код
    assert response.status_code == 200
    assert response.json()['name'] == update_data['name']

def test_current_user(create_user):
    """Тестирование получения текущего пользователя."""
    
    token = get_auth_token(create_user['email'], "password123")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(f'{BASE_URL}/current', headers=headers)
    
    print(f"Current user response status code: {response.status_code}")  # Выводим статус-код
    assert response.status_code == 200
    assert response.json()['email'] == create_user['email']

def test_create_post(create_user):
   """Тестирование создания поста."""
   
   token = get_auth_token(create_user['email'], "password123")
   
   headers = {"Authorization": f"Bearer {token}"}
   
   post_data = {
       "content": "This is a test post."
   }
   
   response = requests.post(f'{BASE_URL}/posts', json=post_data, headers=headers)
   
   print(f"Create post response status code: {response.status_code}")  # Выводим статус-код
   assert response.status_code == 200
   assert 'id' in response.json()

def test_get_all_posts(create_user):
   """Тестирование получения всех постов."""
   
   token = get_auth_token(create_user['email'], "password123")
   
   headers = {"Authorization": f"Bearer {token}"}
   
   response = requests.get(f'{BASE_URL}/posts', headers=headers)
   
   print(f"Get all posts response status code: {response.status_code}")  # Выводим статус-код
   assert response.status_code == 200
   assert isinstance(response.json(), list)

def test_delete_post(create_user):
   """Тестирование удаления поста."""
   
   token = get_auth_token(create_user['email'], "password123")
   
   headers = {"Authorization": f"Bearer {token}"}
   
   post_response = requests.post(f'{BASE_URL}/posts', json={"content": "Post to delete"}, headers=headers)
   post_id = post_response.json()['id']
   
   delete_response = requests.delete(f'{BASE_URL}/posts/{post_id}', headers=headers)
   
   print(f"Delete post response status code: {delete_response.status_code}")  # Выводим статус-код
   assert delete_response.status_code == 200
   assert delete_response.json() is not None
