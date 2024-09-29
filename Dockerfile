# Dockerfile
FROM python:3.12-slim

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install

WORKDIR /app
COPY app ./app/app
COPY main.py ./app/main.py

#RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

CMD ["python3", "-u", "app/main.py"]
