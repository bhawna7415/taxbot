from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.content

def test_chat_app():
    response = client.get("/taxbot?text=Hello")
    assert response.status_code == 200
    assert response

def test_chat_documents():
    response = client.get("/taxbot-vector")
    print(response.text)  # Add this line to see the response content
    assert response.status_code == 200
    assert "Documents successfully inserted" in response.json().get("error", "")