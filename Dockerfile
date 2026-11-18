FROM python:3.13

WORKDIR /code

COPY .pyproject.toml    /code/pyproject.toml

RUN pip install --no-cache-dir .

COPY ./app  /code/app

CMD ["fastapi", "run", "app/main.py", "--port", "80"]