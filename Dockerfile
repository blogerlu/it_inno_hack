# Dockerfile
FROM python:3.12-slim

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install

WORKDIR /app
#COPY src ./src/

#RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

#CMD ["python3", "-u", "src/main.py"]
