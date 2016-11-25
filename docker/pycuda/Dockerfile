# PyCUDA docker image bashed on NVidia CUDA 8.0 + Ubuntu 16.04 x64
# By Xiaohai Li (haixiaolee@gmail.com)
FROM nvidia/cuda:8.0-devel-ubuntu16.04

# Replace with sources from China
RUN echo "deb http://cn.archive.ubuntu.com/ubuntu/ xenial main restricted              "  > /etc/apt/sources.list
RUN echo "deb-src http://cn.archive.ubuntu.com/ubuntu/ xenial main restricted          " >> /etc/apt/sources.list
RUN echo "deb http://cn.archive.ubuntu.com/ubuntu/ xenial-updates main restricted      " >> /etc/apt/sources.list
RUN echo "deb-src http://cn.archive.ubuntu.com/ubuntu/ xenial-updates main restricted  " >> /etc/apt/sources.list
RUN echo "deb http://cn.archive.ubuntu.com/ubuntu/ xenial universe                     " >> /etc/apt/sources.list
RUN echo "deb-src http://cn.archive.ubuntu.com/ubuntu/ xenial universe                 " >> /etc/apt/sources.list
RUN echo "deb http://cn.archive.ubuntu.com/ubuntu/ xenial-updates universe             " >> /etc/apt/sources.list
RUN echo "deb-src http://cn.archive.ubuntu.com/ubuntu/ xenial-updates universe         " >> /etc/apt/sources.list
RUN echo "deb http://cn.archive.ubuntu.com/ubuntu/ xenial-security main restricted     " >> /etc/apt/sources.list
RUN echo "deb-src http://cn.archive.ubuntu.com/ubuntu/ xenial-security main restricted " >> /etc/apt/sources.list
RUN echo "deb http://cn.archive.ubuntu.com/ubuntu/ xenial-security universe            " >> /etc/apt/sources.list
RUN echo "deb-src http://cn.archive.ubuntu.com/ubuntu/ xenial-security universe        " >> /etc/apt/sources.list

# Install dependent packages
RUN apt-get -y update
RUN apt-get install -y wget nano python-pip libboost-all-dev python-numpy
RUN apt-get install -y build-essential python-dev python-setuptools libboost-python-dev libboost-thread-dev

# Compile and install pyCUDA from source
COPY python-pycuda/pycuda-2016.1.2.tar.gz /root/pycuda-2016.1.2.tar.gz
RUN tar xzf /root/pycuda-2016.1.2.tar.gz -C /root
RUN cd /root/pycuda-2016.1.2 && ./configure.py --cuda-root=/usr/local/cuda --cudadrv-lib-dir=/usr/lib/x86_64-linux-gnu --boost-inc-dir=/usr/include --boost-lib-dir=/usr/lib --boost-python-libname=boost_python --boost-thread-libname=boost_thread --no-use-shipped-boost && make -j8 /root/pycuda-2016.1.2 && python setup.py install && pip install .
RUN rm /root/pycuda* -rf
COPY python-pycuda/aescuda.py python-pycuda/cuda_enc.py /root/

CMD nvidia-smi -q && python /root/cuda_enc.py
