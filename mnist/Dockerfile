FROM nvidia/cuda:11.4.3-base-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    git \
    python3-pip \
    python3-dev \
    python3-opencv \
    libglib2.0-0

WORKDIR /app

COPY ./main.py .

RUN pip3 install --no-cache-dir torch==1.12.1 torchvision==0.13.1