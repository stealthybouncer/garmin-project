FROM python:3.11.9-slim

WORKDIR /app

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

ENV NAME=World

CMD ["python", "app.py"]