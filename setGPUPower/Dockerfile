FROM nvidia/cuda:12.8.0-base-ubuntu20.04

WORKDIR /app

COPY ./requirements.txt ./
RUN apt-get update && apt-get install -y nvidia-utils-535 python3 python3-pip
RUN pip install --no-cache-dir -r requirements.txt
COPY ./src ./src
EXPOSE 8080


CMD  ["python3", "./src/setGPUPower.py"]
