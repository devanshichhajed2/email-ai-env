<<<<<<< HEAD
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn pydantic openenv-core

EXPOSE 8000

CMD ["python", "-m", "server.app"]
=======
FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn pydantic openenv-core

EXPOSE 8000

CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
>>>>>>> 9442762521da75db7afedec0a183407fecae9595
