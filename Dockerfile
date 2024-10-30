FROM python:3.12-alpine as compiler

WORKDIR /email-vault-backend

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:/root/.local/bin:$PATH"

RUN apk update && \
    apk add --no-cache gcc musl-dev libpq-dev curl && \
    curl -sSL https://install.python-poetry.org | python3 -

RUN poetry --version

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .

EXPOSE 5000

ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["python3.12", "run.py", "--FLASK_ENV", "${FLASK_ENV}"]
