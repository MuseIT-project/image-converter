FROM python:3.10-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

WORKDIR root
COPY pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root

WORKDIR src
COPY src/ .
COPY pyproject.toml ./stub.toml

EXPOSE 8855
RUN pip install uvicorn
