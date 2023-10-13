FROM python:3.11.4
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN pip3 install poetry==1.6.1
COPY ./pyproject.toml ./poetry.lock ./ 
RUN poetry config virtualenvs.create false  \
    && poetry install
COPY ./src ./src