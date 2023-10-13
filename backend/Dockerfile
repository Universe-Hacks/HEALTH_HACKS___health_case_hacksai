FROM python:3.11.4-alpine
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN apk add --no-cache --virtual .build-deps gcc libffi-dev musl-dev g++
RUN pip3 install poetry==1.6.1
COPY ./pyproject.toml  ./
RUN poetry config virtualenvs.create false  \
    && poetry install
COPY ./src ./src