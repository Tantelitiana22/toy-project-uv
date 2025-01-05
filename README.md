## FIRST PURPOSE UV
This project aim to test uv for managing dependencies.

## requirements:
uv and python 3.11.*

## FASTAPI TOY PROJECT ASYNC
This toy project aim to build a simple example of how to use FastAPI with async functions.
And how to create an integration test with FastAPI based on sqlmodel.

## How to run application:
First run the uv command to install the dependencies:
```bash
uv sync
```
Then run the uv command to start the application:
```bash
uv run uvicorn toy_project.main:app --port 2020
```

## How to test application:

Just run uv pytest command or just pytest