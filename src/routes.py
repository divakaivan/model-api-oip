from fastapi import status, Request, APIRouter
from fastapi.responses import JSONResponse

from src.schemas import (
    InferenceRequestInput,
    InferenceRequestOutput,
    InferenceErrorResponse,
    ModelMetadataResponse,
    ModelMetadataErrorResponse,
    ModelReadyResponse,
    ServerReadyResponse,
    ServerLiveResponse,
    ServerMetadataResponse,
    ServerMetadataErrorResponse,
    MetadataTensor,
    ModelOutput,
)

ROUTER = APIRouter()


@ROUTER.post(
    "/v2/models/petal_classifier/v1/infer",
    response_model=InferenceRequestOutput,
    responses={
        400: {
            "model": InferenceErrorResponse,
            "description": "Error in model inference request",
        }
    },
    tags=["model"],
    description="The /infer endpoint performs inference on a model. The response is the prediction result.",
)
def inference(model_input: InferenceRequestInput, request: Request):
    try:
        ml_models = request.app.state.ml_models

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


@ROUTER.get(
    "/v2/models/petal_classifier/v1",
    response_model=ModelMetadataResponse,
    responses={
        400: {
            "model": ModelMetadataErrorResponse,
            "description": "Error in model metadata request",
        }
    },
    tags=["model"],
    description="The 'model metadata' API is a per-model endpoint that returns details about the model passed in the path.",
)
def model_metadata(request: Request):
    try:
        ml_models = request.app.state.ml_models
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


@ROUTER.get(
    "/v2/models/petal_classifier/v1/ready",
    response_model=ModelReadyResponse,
    tags=["model"],
    description="The “model ready” health API indicates if a specific model is ready for inferencing. The model name and (optionally) version must be available in the URL.",
)
def model_ready(request: Request):
    ml_models = request.app.state.ml_models
    model_name = ml_models["latest_model_info"]["model_name"]
    if "latest_model" in ml_models:
        status_code = status.HTTP_200_OK
        response = ModelReadyResponse(name=model_name, ready=True)
    else:
        status_code = status.HTTP_404_NOT_FOUND
        response = ModelReadyResponse(name=model_name, ready=False)

    return JSONResponse(status_code=status_code, content=response.model_dump())


@ROUTER.get(
    "/v2/health/ready",
    response_model=ServerReadyResponse,
    tags=["server"],
    description="The “server ready” health API indicates if all the models are ready for inferencing.",
)
def server_ready():
    response = ServerReadyResponse(ready=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response.model_dump())


@ROUTER.get(
    "/v2/health/live",
    response_model=ServerLiveResponse,
    tags=["server"],
    description="The “server live” health API indicates if the inference server is able to receive and respond to metadata and inference requests.",
)
def server_live():
    response = ServerLiveResponse(live=True)
    return JSONResponse(status_code=status.HTTP_200_OK, content=response.model_dump())


@ROUTER.get(
    "/v2",
    response_model=ServerMetadataResponse,
    responses={
        400: {
            "model": ServerMetadataErrorResponse,
            "description": "Error in server metadata request",
        }
    },
    tags=["server"],
    description="The 'server metadata' API returns details describing the server.",
)
def server_metadata(request: Request):
    try:
        ml_models = request.app.state.ml_models
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
