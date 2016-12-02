# Start with cuDNN base image
FROM nvidia/cuda:8.0-cudnn5-devel-ubuntu16.04

# Install basic deps
RUN apt-get update && apt-get install -y nano sudo wget build-essential cmake curl gfortran git  \
  libatlas-dev libavcodec-dev libavformat-dev libboost-all-dev libgtk2.0-dev libjpeg-dev   \
  liblapack-dev libswscale-dev pkg-config python-dev python-pip software-properties-common \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN git clone https://github.com/torch/distro.git /root/torch --recursive && cd /root/torch && \
  bash install-deps

RUN cd /root/torch && ./install.sh

ENV PATH=$PATH:'/root/torch/install/bin/'

RUN luarocks install cutorch && luarocks install cunn && luarocks install cudnn

WORKDIR /root
