import pytest
from fastapi.testclient import TestClient
from src.main import app


# Fixture for FastAPI test client
@pytest.fixture
def client() -> TestClient:
    app.state.ml_models = {
        "latest_model": DummyModel(),
        "latest_model_info": {
            "model_name": "petal_classifier",
            "model_version": "v1",
            "model_platform": "sklearn",
            "model_input_signature": [
                {"name": "petal length (cm)", "shape": [1], "datatype": "FP32"},
                {"name": "petal width (cm)", "shape": [1], "datatype": "FP32"},
            ],
            "model_output_signature": [
                {"name": "class", "shape": [1], "datatype": "INT64"},
            ],
        },
    }

    with TestClient(app) as client:
        yield client


class DummyModel:
    def predict(self, features):
        return [1]  # always predict 1
