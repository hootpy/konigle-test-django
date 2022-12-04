FROM python:3.10-slim-buster as builder

RUN pip install "poetry==1.2.2"

WORKDIR /konigle

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

FROM python:3.10-slim-buster

COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/


WORKDIR /konigle
COPY ./app ./app
WORKDIR /konigle/app
