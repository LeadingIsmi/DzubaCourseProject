FROM python:3.12
WORKDIR /app

RUN pip install motor "fastapi[all]" requests

COPY . /app

ENTRYPOINT ["bash", "-c", "uvicorn main:app --port 8080 --host 0.0.0.0"]