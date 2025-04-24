from pydantic import BaseModel, Field


class ModelReadyResponse(BaseModel):
    name: str = Field(description="The name of the model.")
    ready: bool = Field(
        description="True if the model is ready to accept requests, false otherwise."
    )


class ServerReadyResponse(BaseModel):
    ready: bool = Field(
        description="True if the server is ready to accept requests, false otherwise."
    )


class ServerLiveResponse(BaseModel):
    live: bool = Field(description="True if the server is live, false otherwise.")


class ServerMetadataResponse(BaseModel):
    name: str = Field(description="A descriptive name for the server.")
    version: str = Field(description="The server version.")
    extensions: list[str] | None = Field(
        default=None,
        description="The extensions supported by the server. Currently, no standard extensions are defined. Individual inference servers may define and document their own extensions.",
    )


class ServerMetadataErrorResponse(BaseModel):
    error: str = Field(description="The descriptive message for the error.")


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


class ModelInput(BaseModel):
    name: str = Field(description="The name of the input tensor.")
    shape: list[int] = Field(
        description="The shape of the input tensor. Each dimension must be an integer representable as an unsigned 64-bit integer value."
    )
    datatype: str = Field(description="The data-type of the input tensor elements.")
    data: float = Field(description="The contents of the tensor.")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "petal length (cm)",
                "shape": [1],
                "datatype": "FP32",
                "data": 4.5,
            }
        }
    }


class InferenceRequestInput(BaseModel):
    id: str = Field(
        description="An identifier for this request. Optional, but if specified this identifier must be returned in the response."
    )
    inputs: list[ModelInput] = Field(
        description="The input tensors. Each input is described using the ModelInput"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "inference-123",
                "inputs": [
                    {
                        "name": "petal length (cm)",
                        "shape": [1],
                        "datatype": "FP32",
                        "data": 4.5,
                    },
                    {
                        "name": "petal width (cm)",
                        "shape": [1],
                        "datatype": "FP32",
                        "data": 1.2,
                    },
                ],
            }
        }
    }


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