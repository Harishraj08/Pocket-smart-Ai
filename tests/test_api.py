import os
os.environ["AI_MODE"]="mock"
os.environ["DATABASE_URL"]="sqlite:///./data/test_pocketsmart.db"
os.environ["SECRET_KEY"]="test-secret-key-with-at-least-32-characters"
from fastapi.testclient import TestClient
from app.main import app
from app.database import init_db,get_conn
init_db()
client=TestClient(app)
def test_health():
    r=client.get("/api/health");assert r.status_code==200 and r.json()["status"]=="ok"
def test_home():
    r=client.post("/api/generate-home",json={"budget":50000,"room":"Living Room","items":[{"category":"lighting","quantity":2,"style":"modern"}],"priorities":[]})
    assert r.status_code==200 and r.json()["estimated_total"]<=50000
def test_party():
    r=client.post("/api/generate-party",json={"budget":50000,"guests":20,"event_type":"Birthday","venue":"Home","city":"Dindigul","priorities":[]})
    assert r.status_code==200
def test_jewelry():
    r=client.post("/api/generate-jewelry",data={"budget":"10000","occasion":"Wedding","style":"Minimal","color_preference":"Gold"})
    assert r.status_code==200 and r.json()["planner"]=="jewelry"
def test_auth():
    email="test-user@example.com"
    with get_conn() as c:c.execute("DELETE FROM users WHERE email=?",(email,))
    r=client.post("/api/auth/register",json={"email":email,"name":"Test User","password":"password123"})
    assert r.status_code==201
    assert client.get("/api/auth/me").status_code==200
    client.post("/api/auth/logout")
    assert client.get("/api/auth/me").status_code==401
