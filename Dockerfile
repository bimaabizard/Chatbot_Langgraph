# Use python slim image
FROM python:3.11-slim-bookworm

# Install uv for fast dependency resolution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install dependencies first (caching layer)
COPY pyproject.toml ./
RUN uv pip install --system -r pyproject.toml

# Copy application code
COPY ./app ./app

# Expose API port
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]