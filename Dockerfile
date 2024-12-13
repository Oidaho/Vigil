FROM python:3.12-slim

WORKDIR /

RUN pip install poetry

COPY ./pyptoject.toml .

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-interaction --no-ansi

COPY . .

EXPOSE 8080

CMD [ "poetry", "run", "python", "main.py" ]