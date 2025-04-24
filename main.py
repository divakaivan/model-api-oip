import joblib
from fastapi import FastAPI

app = FastAPI()

@app.post("/predict")
def predict(data: dict):

    model = joblib.load("petal_model.joblib")
    prediction = model.predict([[data["petal length (cm)"], data["petal width (cm)"]]])

    return {"prediction": int(prediction[0])}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
