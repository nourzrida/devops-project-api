from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur l'API DevOps Quotes !"}

def test_create_quote():
    payload = {"author": "Tester", "text": "Automation is key"}
    response = client.post("/quotes", json=payload)
    assert response.status_code == 201
    assert response.json()["author"] == "Tester"