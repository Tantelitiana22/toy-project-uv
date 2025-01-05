FROM python:3.12-slim-bullseye

WORKDIR /application

COPY requirements.txt .

RUN pip install --upgrade pip \
  && pip install -r requirements.txt

COPY app ./app
COPY main.py .

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" ]
