FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn pydantic openenv-core

EXPOSE 8000

CMD ["python", "-m", "server.app"]