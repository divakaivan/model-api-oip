from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
