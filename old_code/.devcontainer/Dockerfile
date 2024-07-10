# This Dockerfile sets up a Python 3.11 environment with Poetry for a Garmin project.
# It creates a non-root user, installs project dependencies, and sets up the working directory.
# Finally, it starts the application using Uvicorn with the specified host, port, and proxy headers.

FROM python:3.11-bookworm

RUN useradd lclusr
ARG APP_DIR="/garmin"
RUN mkdir ${APP_DIR}
RUN chown -R lclusr:lclusr ${APP_DIR}
WORKDIR ${APP_DIR}

# Install poetry
RUN pip install poetry

COPY pyproject.toml ${APP_DIR}/
RUN poetry env use 3.11 &&\
    poetry config virtualenvs.path ${APP_DIR}/virtualenvs &&\
    poetry config virtualenvs.in-project true &&\
    poetry install

ENV PYTHONPATH ${APP_DIR}
COPY src ${APP_DIR}/src
COPY config ${APP_DIR}/config

RUN mkdir ${APP_DIR}/logs
RUN chown -R lclusr:lclusr ${APP_DIR}/logs
RUN chmod 755 ${APP_DIR}/logs/
USER lclusr

CMD poetry run uvicorn --app-dir src main:app --host 0.0.0.0 --port 8090 --proxy-headers
