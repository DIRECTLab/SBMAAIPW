FROM python:3.11-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN apt-get update && apt-get install -y swig build-essential
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src ./src
EXPOSE 8080

CMD  ["python", "./src/main.py"]
