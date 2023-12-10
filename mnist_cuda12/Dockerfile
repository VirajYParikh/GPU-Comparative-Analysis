FROM nvidia/cuda:12.0.0-base-ubuntu20.04

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

RUN pip3 install torch==2.1.0 torchvision==0.16.0