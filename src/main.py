from fastapi import FastAPI
import yaml
from contextlib import asynccontextmanager
from src.routes import ROUTER


@asynccontextmanager
async def lifespan(app: FastAPI):
    import joblib

    with open("src/model_info.yaml", "r") as f:
        model_info = yaml.safe_load(f)

    app.state.ml_models = {}
    app.state.ml_models["latest_model_info"] = model_info
    app.state.ml_models["latest_model"] = joblib.load(model_info["model_path"])

    yield

    app.state.ml_models.clear()


tags_metadata = [
    {
        "name": "model",
        "description": "Endpoints related to the ML model.",
    },
    {
        "name": "server",
        "description": "Endpoints related to the Server",
    },
]


def create_app() -> FastAPI:
    """Create a FastAPI application."""
    app = FastAPI(
        title="Petal Classifier Model API",
        description=(
            "API following the [Open Inference Protocol v2]"
            "(https://kserve.github.io/website/latest/modelserving/data_plane/v2_protocol/#open-inference-protocol-v2-inference-protocol)"
        ),
        lifespan=lifespan,
        docs_url="/",
        redoc_url=None,
        version="1.0.0",
        openapi_tags=tags_metadata,
    )

    app.include_router(ROUTER)

    return app


if __name__ == "__main__":
    import uvicorn

    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)
