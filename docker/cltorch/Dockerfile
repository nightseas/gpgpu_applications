# Start with cuDNN base image
FROM nvidia/cuda:8.0-cudnn5-devel-ubuntu16.04

# Install basic deps
RUN apt-get update && apt-get install -y nano sudo wget build-essential cmake curl gfortran git  \
  libatlas-dev libavcodec-dev libavformat-dev libboost-all-dev libgtk2.0-dev libjpeg-dev   \
  liblapack-dev libswscale-dev pkg-config python-dev python-pip software-properties-common \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install NV drivers and openCL lib
RUN apt-get update && apt-get install -y nvidia-367 nvidia-367-dev nvidia-opencl-icd-367 nvidia-settings \
  && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Fetch and install cltorch
RUN git clone --recursive https://github.com/hughperkins/distro -b distro-cl ~/torch-cl && cd ~/torch-cl && bash install-deps

# Do not use gcc4.9! There's compatibility issues between gcc4.9, boost, and dlib
RUN cd ~/torch-cl && sed -i -- 's/gcc-4.9/gcc/g' install.sh && sed -i -- 's/g++-4.9/g++/g' install.sh && ./install.sh

WORKDIR /root
