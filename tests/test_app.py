import pytest

from app import create_app


@pytest.fixture
def client(tmp_path):
    app = create_app(str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    return app.test_client()


def test_health(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_submit_and_display(client):
    resp = client.post(
        "/",
        data={"name": "Asha", "course": "DevOps", "feedback": "Great labs!"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Asha" in body and "DevOps" in body and "Great labs!" in body


def test_missing_field_rejected(client):
    resp = client.post("/", data={"name": "Asha", "course": "", "feedback": "x"})
    assert "All fields are required" in resp.get_data(as_text=True)


def test_html_is_escaped(client):
    client.post("/", data={"name": "<script>x</script>", "course": "C", "feedback": "f"})
    assert "<script>x</script>" not in client.get("/").get_data(as_text=True)
