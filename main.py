import joblib
from fastapi import FastAPI

app = FastAPI()

@app.post("/predict")
def predict(data: dict):

    # TODO
    # use joblib to load the model
    # expected model inputs: 
    #   petal length (cm): float
    #   petal width (cm): float
    # model output:
    #   iris species: int (0, 1, 2)

    return {"prediction": int(prediction[0])}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
