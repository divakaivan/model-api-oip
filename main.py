from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager
import yaml

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    import joblib

    with open("model_info.yaml", "r") as f:
        model_info = yaml.safe_load(f)

    ml_models["latest_model_info"] = model_info
    ml_models["latest_model"] = joblib.load(model_info["model_path"])

    yield

    ml_models.clear()

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
    tags=["server"]
)
def server_ready():
    response = ServerReadyResponse(ready=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response.model_dump())

#########################################
######### /v2/health/live ###############
#########################################

class ServerLiveResponse(BaseModel):
    live: bool = Field(description="True if the server is live, false otherwise.")


@app.get(
    "/v2/health/live",
    response_model=ServerLiveResponse,
    description="The “server live” health API indicates if the inference server is able to receive and respond to metadata and inference requests.",
    tags=["server"]
)
def server_live():
    response = ServerLiveResponse(live=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response.model_dump())


#############################################################
######### /v2/models/petal_classifier/v1/ready ##############
#############################################################

class ModelReadyResponse(BaseModel):
    name: str = Field(description="The name of the model.")
    ready: bool = Field(
        description="True if the model is ready to accept requests, false otherwise."
    )


@app.get(
    "/v2/models/petal_classifier/v1/ready",
    response_model=ModelReadyResponse,
    description="The “model ready” health API indicates if a specific model is ready for inferencing. The model name and (optionally) version must be available in the URL.",
    tags=["model"]
)
def model_ready():
    model_name = ml_models["latest_model_info"]["model_name"]
    if "latest_model" in ml_models:
        status_code = status.HTTP_200_OK
        response = ModelReadyResponse(name=model_name, ready=True)
    else:
        status_code = status.HTTP_404_NOT_FOUND
        response = ModelReadyResponse(name=model_name, ready=False)

    return JSONResponse(status_code=status_code, content=response.model_dump())


############################
######### /v2 ##############
############################

class ServerMetadataResponse(BaseModel):
    name: str = Field(description="A descriptive name for the server.")
    version: str = Field(description="The server version.")
    extensions: list[str] | None = Field(
        default=None,
        description="The extensions supported by the server. Currently, no standard extensions are defined. Individual inference servers may define and document their own extensions.",
    )

class ServerMetadataErrorResponse(BaseModel):
    error: str = Field(description="The descriptive message for the error.")


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
    tags=["server"],
)
def server_metadata():
    try:
        response = ServerMetadataResponse(
            name=f"{ml_models['latest_model_info']['model_name']} Inference Server",
            version=f"{ml_models['latest_model_info']['model_version']}",
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK, content=response.model_dump()
        )
    except Exception as e:
        error_response = ServerMetadataErrorResponse(error=str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=error_response.model_dump()
        )

#######################################################
######### /v2/models/petal_classifier/v1 ##############
#######################################################

class MetadataTensor(BaseModel):
    name: str = Field(description="The name of the tensor.")
    datatype: str = Field(description="The data-type of the tensor elements.")
    shape: list[int] = Field(
        description="The shape of the tensor. Variable-size dimensions are specified as -1."
    )


class ModelMetadataResponse(BaseModel):
    name: str = Field(description="The name of the model.")
    versions: list[str] | None = Field(
        default=None,
        description="The model versions that may be explicitly requested via the appropriate endpoint. Optional for servers that don’t support versions. Optional for models that don’t allow a version to be explicitly requested.",
    )
    platform: str = Field(description="The framework/backend for the model.")
    inputs: list[MetadataTensor] = Field(
        description="The inputs required by the model."
    )
    outputs: list[MetadataTensor] = Field(
        description="The outputs produced by the model."
    )


class ModelMetadataErrorResponse(BaseModel):
    error: str = Field(description="The descriptive message for the error.")


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
    tags=["model"],
)
def model_metadata():
    try:
        model_info = ml_models["latest_model_info"]
        response = ModelMetadataResponse(
            name=model_info["model_name"],
            versions=[model_info["model_version"]],
            platform=model_info["model_platform"],
            inputs=[
                MetadataTensor(**tensor)
                for tensor in model_info["model_input_signature"]
            ],
            outputs=[
                MetadataTensor(**tensor)
                for tensor in model_info["model_output_signature"]
            ],
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK, content=response.model_dump()
        )

    except Exception as e:
        error_response = ModelMetadataErrorResponse(error=str(e))

        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=error_response.model_dump()
        )

######################################################
######### /v2/models/petal_classifier/v1/infer #######
######################################################


class ModelInput(BaseModel):
    name: str = Field(description="The name of the input tensor.")
    shape: list[int] = Field(
        description="The shape of the input tensor. Each dimension must be an integer representable as an unsigned 64-bit integer value."
    )
    datatype: str = Field(description="The data-type of the input tensor elements.")
    data: float = Field(description="The contents of the tensor.")


class InferenceRequestInput(BaseModel):
    id: str = Field(
        description="An identifier for this request. Optional, but if specified this identifier must be returned in the response."
    )
    inputs: list[ModelInput] = Field(
        description="The input tensors. Each input is described using the ModelInput"
    )

    

class ModelOutput(BaseModel):
    name: str = Field(description="The name of the output tensor.")
    shape: list[int] = Field(
        description="The shape of the output tensor. Each dimension must be an integer representable as an unsigned 64-bit integer value."
    )
    datatype: str = Field(description="The data-type of the output tensor elements.")
    data: int = Field(description="The contents of the tensor.")


class InferenceRequestOutput(BaseModel):
    model_name: str = Field(description="The name of the model used for inference.")
    model_version: str | None = Field(
        default=None,
        description="The specific model version used for inference. Inference servers that do not implement versioning should not provide this field in the response.",
    )
    id: str = Field(description="The 'id' identifier given in the request, if any.")
    outputs: list[ModelOutput] = Field(
        description="The output tensors. Each output is described using the ModelOutput."
    )


class InferenceErrorResponse(BaseModel):
    error: str = Field(description="The descriptive message for the error.")


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
    tags=["model"],
)
def inference(model_input: InferenceRequestInput):
    try:

        model = ml_models.get("latest_model")
        model_info = ml_models.get("latest_model_info")
        if not model or not model_info:
            error_response = InferenceErrorResponse(error="Model not loaded yet")
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=error_response.model_dump(),
            )

        input_dict = {inp.name: inp.data for inp in model_input.inputs}

        required_inputs = ["petal length (cm)", "petal width (cm)"]
        for required in required_inputs:
            if required not in input_dict:
                error_response = InferenceErrorResponse(
                    error=f"Required input missing {required}"
                )
                return JSONResponse(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    content=error_response.model_dump(),
                )

        features = [
            float(input_dict["petal length (cm)"]),
            float(input_dict["petal width (cm)"]),
        ]

        prediction = model.predict([features])[0]

        output_signature = model_info["model_output_signature"][0]
        output = ModelOutput(
            name=output_signature["name"],
            shape=output_signature["shape"],
            datatype=output_signature["datatype"],
            data=int(prediction),
        )

        response = InferenceRequestOutput(
            model_name=model_info["model_name"],
            model_version=model_info["model_version"],
            id=model_input.id,
            outputs=[output],
        )

        return JSONResponse(
            status_code=status.HTTP_200_OK, content=response.model_dump()
        )

    except Exception as e:
        error_response = InferenceErrorResponse(error=str(e))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST, content=error_response.model_dump()
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
