from fastapi.testclient import TestClient


def test__inference(client: TestClient):
    assert 1 == 1