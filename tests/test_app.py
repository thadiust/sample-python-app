from app import app


def test_home_returns_hello_world() -> None:
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200  # nosec B101
    assert resp.text == "Hello, world!"  # nosec B101
