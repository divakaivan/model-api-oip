# 4/restructure-start

Our API starts to take form. But it's not that good that all the code is in `main.py`. 

For this part, I invite you to read the FastAPI docs about [Bigger Applications - Multiple Files](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

Reading the docs will help you understand the need to restructure our current app into more managable smaller files.

The goal for this chapter is to end up with a structure like:

```bash
src/
  | - main.py # containing the FastAPI app
  | - model_info.yaml
  | - petal_model.joblib
  | - routes.py # NEW: containing the http endpoints
  | - schemas.py # NEW: containing the Pydantic schemas

requirements.txt
.gitignore
```

Also, instead of loading the `petal_model.joblib` and `model_info.yaml` into a dictionary, we can use "state" - [read more here](https://fastapi.tiangolo.com/reference/fastapi/#fastapi.FastAPI.state)

See you in the branch `4/restructure-completed`