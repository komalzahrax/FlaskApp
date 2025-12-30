from app import app

def test_home_page_loads():
    app.config["TESTING"] = True
    client = app.test_client()
    r = client.get("/")
    assert r.status_code == 200
