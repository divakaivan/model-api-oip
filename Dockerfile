FROM python:3.13-alpine

WORKDIR /app

RUN apk add --no-cache gcc g++ musl-dev libffi-dev build-base

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.main:create_app", "--host", "0.0.0.0", "--port", "8000"]
