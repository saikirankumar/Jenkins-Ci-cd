from app import app, add

def test_add():
    assert add(2, 3) == 5

def test_health():
    assert app.test_client().get("/health").json["status"] == "ok"
