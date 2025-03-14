FROM ubuntu:22.04 AS base
WORKDIR /root
RUN apt update && \
    apt -y install software-properties-common git python3-pip && \
    git clone https://github.com/lulinpeng/FileQrcoder.git && cd FileQrcoder/ && \
    pip3 install -r requirements.txt
