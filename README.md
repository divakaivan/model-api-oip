# 1/setup-completed

If you skipped the 1/setup-start, please check the below instructions.

Clone the repo from the starting point branch

- `git clone git clone -b 1/setup-completed  https://github.com/user/repository.git`

Create a new venv

- `python -m venv venv`

Install requirements

- `pip install --no-cache-dir -r requirements.txt`

We will install all the dependencies at once so we don't have to deal with them down the line. The main ones that we'll be using are `joblib, scikit-learn, fastapi, pytest, pre-commit, httpx, pydantic, PyYAML, uvicorn`. The rest are sub-dependencies of these main ones. 

Try running the API server

- `python main.py`

You should have access to the docs on `http://0.0.0.0:8000/docs`. Try querying the `/predict` endpoint by passing the below json as the request body

```json
{
  "petal length (cm)": 2.5,
  "petal width (cm)": 2.0
}
```

You should get a response with status 200 and response body like

```json
{
  "prediction": 2
}
```

You can move on to the tasks from branch `2/endpoints-start`