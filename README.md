# Take your ML model APIs to the next level

## From `/predict` to the Open Inference Protocol

Take your basic `/predict` ML model APIs to the next level:

- design them following the [Open Inference Protocol](https://kserve.github.io/website/latest/modelserving/data_plane/v2_protocol/) — a growing industry standard for standardized, observable, and interoperable machine learning inference
- auto-documentation using FastAPI and Pydantic
- add linting, testing and pre-commit hooks
- build and push an Docker image of the API to Docker Hub
- use Github Actions for automation

## End result

![docs](docs.png)

#### HTTP/REST endpoints

| API             | Verb | Path                                                       |
|------------------|------|------------------------------------------------------------|
| Inference        | POST | v2/models/[/versions/<model_version>]/infer               |
| Model Metadata   | GET  | v2/models/<model_name>[/versions/<model_version>]         |
| Server Ready     | GET  | v2/health/ready                                           |
| Server Live      | GET  | v2/health/live                                            |
| Server Metadata  | GET  | v2                                                       |
| Model Ready      | GET  | v2/models/<model_name>[/versions/]/ready                 |

#### API Definitions

| API             | Definition                                                                                                                                                              |
|------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Inference        | The `/infer` endpoint performs inference on a model. The response is the prediction result.                                                                             |
| Model Metadata   | The "model metadata" API is a per-model endpoint that returns details about the model passed in the path.                                                              |
| Server Ready     | The “server ready” health API indicates if all the models are ready for inferencing. The “server ready” health API can be used directly to implement the Kubernetes readinessProbe. |
| Server Live      | The “server live” health API indicates if the inference server is able to receive and respond to metadata and inference requests. The “server live” API can be used directly to implement the Kubernetes livenessProbe. |
| Server Metadata  | The "server metadata" API returns details describing the server.                                                                                                        |
| Model Ready      | The “model ready” health API indicates if a specific model is ready for inferencing. The model name and (optionally) version must be available in the URL.             |
