FROM python:3.11-bookworm

ARG version

RUN useradd lclusr
ARG APP_DIR="/garmin"
RUN mkdir ${APP_DIR}
RUN chown -R lclusr:lclusr ${APP_DIR}
WORKDIR ${APP_DIR}

COPY pyproject.toml ${APP_DIR}/
RUN poetry env use 3.11 && \
    poetry config virutalenvs.path ${APP_DIR}/virutalenvs && \
    poetry config virutalenvs.in-project true && \
    poetry install

ENV PYTHONPATH ${APP_DIR}
COPY src ${APP_DIR}/src
COPY config ${APP_DIR}/config

RUN mkdir ${APP_DIR}/logs
RUN chown -R lclusr:lclusr ${APP_DIR}/logs
RUN chmod 755 ${APP_DIR}/logs/
USER lclusr

CMD poetry run uvicorn --app-dir src main:app --host 0.0.0.0 --port 8090 --proxy-headers
