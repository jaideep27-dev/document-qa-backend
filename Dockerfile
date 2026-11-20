FROM python:3.12.3-slim AS base

# prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /code

# Install dependencies first for layer caching
COPY pyproject.toml .

# Create a placeholder package structure if your build backend requires it during install,
# or install dependencies directly first for better caching:

RUN pip install --no-cache-dir --upgrade pip \
    && python -c 'import tomllib, subprocess; deps = tomllib.load(open("pyproject.toml", "rb")).get("project", {}).get("dependencies", []); subprocess.run(["pip", "install", "--no-cache-dir", *deps], check=True)'

# Create non-root user and copy application code
RUN adduser --disabled-password --gecos "" appuser
COPY --chown=appuser:appuser ./app /code/app

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]