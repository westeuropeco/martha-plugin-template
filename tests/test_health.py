"""Smoke tests for __PLUGIN_DISPLAY__ BFF."""

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_health_returns_ok() -> None:
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_things_round_trip() -> None:
    create = client.post("/things", json={"name": "demo", "description": "hello"})
    assert create.status_code == 201
    thing_id = create.json()["id"]

    listing = client.get("/things")
    assert any(t["id"] == thing_id for t in listing.json())

    deletion = client.delete(f"/things/{thing_id}")
    assert deletion.status_code == 204
    assert client.get(f"/things/{thing_id}").status_code == 404


def test_openapi_carries_martha_extensions() -> None:
    schema = client.get("/openapi.json").json()
    assert schema["x-martha-integration"]["type"] == "plugin"
    assert schema["x-martha-plugin"]["name"] == "__PLUGIN_NAME__"
    paths = [r["path"] for r in schema["x-martha-plugin"]["resources"]]
    assert "/things" in paths
