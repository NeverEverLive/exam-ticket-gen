FROM python:3.11-slim

RUN apt-get --yes update &&\
    apt-get --yes install libopenblas-dev libomp-dev build-essential curl


ENV PATH="${PATH}:${HOME}/.local/bin"
RUN pip install -U pip && pip install setuptools && pip install poetry==1.3.2

COPY /src /app/src
COPY poetry.lock pyproject.toml README.md /app/

WORKDIR /app

RUN poetry build
RUN pip install ./dist/*.tar.gz

CMD ["uvicorn", "--factory", "src.app:create_app", "--host", "0.0.0.0", "--port", "8000", "--workers", "6"]