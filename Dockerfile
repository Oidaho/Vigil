FROM python:3.12-slim

WORKDIR /

RUN pip install poetry

COPY ./pyproject.toml .

RUN poetry config virtualenvs.create false && poetry install --only main --no-interaction --no-ansi

COPY . .

CMD [ "python", "main.py" ]