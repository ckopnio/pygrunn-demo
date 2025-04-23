FROM python:3.12

RUN pip install uv

WORKDIR /app

COPY src/cdc_demo /app/cdc_demo
COPY pyproject.toml /app/

RUN uv pip install --system -e .

ENV PYTHONPATH="${PYTHONPATH}:/app"
