from fastapi.testclient import TestClient


def test__inference_model_not_loaded(client: TestClient):
    client.app.state.ml_models = {}

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

    assert response.status_code == 404
    assert "Model not loaded yet" in response.json()["error"]


def test__inference_missing_required_input(client: TestClient):
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
                }
            ],
        },
    )

    assert response.status_code == 422
    assert "Required input missing petal width (cm)" in response.json()["error"]


def test__model_metadata_model_info_missing(client: TestClient):
    client.app.state.ml_models = {}

    response = client.get("/v2/models/petal_classifier/v1")
    assert response.status_code == 400
    assert "error" in response.json()


def test__model_ready_model_not_loaded(client: TestClient):
    client.app.state.ml_models = {
        "latest_model_info": {"model_name": "petal_classifier"}
    }

    response = client.get("/v2/models/petal_classifier/v1/ready")
    assert response.status_code == 404
    assert response.json()["ready"] is False


def test__server_metadata_failure(client: TestClient):
    client.app.state.ml_models = {}

    response = client.get("/v2")
    assert response.status_code == 400
    assert "error" in response.json()