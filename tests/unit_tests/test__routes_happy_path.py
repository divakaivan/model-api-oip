from fastapi.testclient import TestClient


def test__inference(client: TestClient):
    response = client.post(
        "/v2/models/petal_classifier/v1/infer",
        json={
            "id": "test-id",
            "inputs": [
                {
                    "name": "petal length (cm)",
                    "shape": [1],
                    "datatype": "FP32",
                    "data": 3.5,
                },
                {
                    "name": "petal width (cm)",
                    "shape": [1],
                    "datatype": "FP32",
                    "data": 1.2,
                },
            ],
        },
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["model_name"] == "petal_classifier"
    assert json_data["outputs"][0]["data"] == 1


def test__model_metadata(client: TestClient):
    response = client.get("/v2/models/petal_classifier/v1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "petal_classifier"
    assert data["versions"] == ["v1"]
    assert isinstance(data["inputs"], list)
    assert isinstance(data["outputs"], list)


def test__model_ready(client: TestClient):
    response = client.get("/v2/models/petal_classifier/v1/ready")
    assert response.status_code == 200
    assert response.json()["ready"] is True


def test__server_ready(client: TestClient):
    response = client.get("/v2/health/ready")
    assert response.status_code == 200
    assert response.json()["ready"] is True


def test__server_live(client: TestClient):
    response = client.get("/v2/health/live")
    assert response.status_code == 200
    assert response.json()["live"] is True


def test__server_metadata(client: TestClient):
    response = client.get("/v2")
    assert response.status_code == 200
    data = response.json()
    assert "Inference Server" in data["name"]
    assert data["version"] == "v1"
