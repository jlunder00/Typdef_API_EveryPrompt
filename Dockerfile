# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
WORKDIR app/
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY app/ src/
WORKDIR src/
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "main:app",  "--host", "0.0.0.0", "--port", "8080", "--reload"]