FROM ubuntu:22.04 AS base
WORKDIR /root
RUN apt update && \
    apt -y install software-properties-common git python3-pip vim && \
    apt -y install libzbar0 libzbar-dev && \
    git clone https://github.com/lulinpeng/FileQrcoder.git && cd FileQrcoder/ && \
    pip3 install -r requirements.txt
