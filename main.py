from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import yaml

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    import joblib

    with open("src/model_info.yaml", "r") as f:
        model_info = yaml.safe_load(f)

    ml_models["latest_model_info"] = model_info
    ml_models["latest_model"] = joblib.load(model_info["model_path"])

    # above yield are ran on startup
    yield
    # below yield are ran on shutdown

    ml_models.clear()

app = FastAPI()


############################################
######### /v2/health/ready #################
############################################

class ServerReadyResponse(BaseModel):
    ready: bool = Field(
        description="True if the server is ready to accept requests, false otherwise."
    )

@app.get(
    "/v2/health/ready",
    response_model=ServerReadyResponse,
    description="The “server ready” health API indicates if all the models are ready for inferencing.",
)
def server_ready():
    response = ServerReadyResponse(ready=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response.model_dump())

#########################################
######### /v2/health/live ###############
#########################################

class ServerLiveResponse(BaseModel):
    ...


@app.get(
    "/v2/health/live",
    response_model=ServerLiveResponse,
    description="The “server live” health API indicates if the inference server is able to receive and respond to metadata and inference requests.",
)
def server_live():
    ...


#############################################################
######### /v2/models/petal_classifier/v1/ready ##############
#############################################################

class ModelReadyResponse(BaseModel):
    ...


@app.get(
    "/v2/models/petal_classifier/v1/ready",
    response_model=ModelReadyResponse,
    description="The “model ready” health API indicates if a specific model is ready for inferencing. The model name and (optionally) version must be available in the URL.",
)
def model_ready():
    ...


############################
######### /v2 ##############
############################

class ServerMetadataResponse(BaseModel):
    ...

class ServerMetadataErrorResponse(BaseModel):
    ...


@app.get(
    "/v2",
    response_model=ServerMetadataResponse,
    responses={
        400: {
            "model": ServerMetadataErrorResponse,
            "description": "Error in server metadata request",
        }
    },
    description="The 'server metadata' API returns details describing the server.",
)
def server_metadata():
    ...

#######################################################
######### /v2/models/petal_classifier/v1 ##############
#######################################################

class MetadataTensor(BaseModel):
    ...

class ModelMetadataResponse(BaseModel):
    ...


class ModelMetadataErrorResponse(BaseModel):
    ...


@app.get(
    "/v2/models/petal_classifier/v1",
    response_model=ModelMetadataResponse,
    responses={
        400: {
            "model": ModelMetadataErrorResponse,
            "description": "Error in model metadata request",
        }
    },
    description="The 'model metadata' API is a per-model endpoint that returns details about the model passed in the path.",
)
def model_metadata():
    ...

######################################################
######### /v2/models/petal_classifier/v1/infer #######
######################################################

class ModelInput(BaseModel):
    ...

class InferenceRequestInput(BaseModel):
    ...

class ModelOutput(BaseModel):
    ...


class InferenceRequestOutput(BaseModel):
    ...


class InferenceErrorResponse(BaseModel):
    ...

@app.post(
    "/v2/models/petal_classifier/v1/infer",
    response_model=InferenceRequestOutput,
    responses={
        400: {
            "model": InferenceErrorResponse,
            "description": "Error in model inference request",
        }
    },
    description="The /infer endpoint performs inference on a model. The response is the prediction result.",
)
def inference(model_input: InferenceRequestInput):
    ...


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
