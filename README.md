# 4/restructure-completed

I hope you read the FastAPI docs page about bigger applications with multiple files. 

In `routes.py` I defined a `ROUTER = APIRouter()` which I use on the endpoints. Instead of `app.get(...)`, now we have `ROUTER.get(...)`. And then we import this `ROUTER` into `main.py` and pass it so the FastAPI `app` can use it: `app.include_router(ROUTER)`

In addition, the lifespan now initialises the model info dict and model file into the app's state. To access this state from the different endpoints, we add a `request: Request` as a parameter, and get the item like: `ml_models = request.app.state.ml_models`

### IMPORTANT!!!

Now that we have restructured, make sure to update the paths to the model joblib file and the model info yaml file like:

- `with open("src/model_info.yaml", "r")` in `main.py`'s `lifespan`
- `model_path: "src/petal_model.joblib"` in `model_info.yaml`

Now we can run the app from the root dir using `python -m src.main`