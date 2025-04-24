# 1/setup-start

Clone the repo from the starting point branch

- `git clone git clone -b 1/setup-start  https://github.com/user/repository.git`

Create a new venv

- `python -m venv venv`

Install requirements

- `pip install --no-cache-dir -r requirements.txt`

We will install all the dependencies at once so we don't have to deal with them down the line. The main ones that we'll be using are `joblib, scikit-learn, fastapi, pytest, pre-commit, httpx, pydantic, PyYAML, uvicorn`. The rest are sub-dependencies of these main ones. 

Open `main.py` and try completing the POST `/predict` endpoint. You don't need to struggle too much, feel free to check the code in the branch `1/setup-completed`.
