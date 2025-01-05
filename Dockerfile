FROM python:3.11-slim-bullseye

WORKDIR /application

COPY pyproject.toml uv.lock ./

COPY --from=ghcr.io/astral-sh/uv:0.5.14 /uv /uvx /bin/
RUN uv sync --frozen

COPY src/toy_project ./toy_project
ENTRYPOINT ["uv", "run","uvicorn", "toy_project.main:app", "--host", "0.0.0.0", "--port", "2020" ]
