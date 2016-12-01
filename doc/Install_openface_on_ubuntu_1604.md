# Install Openface on Ubuntu 16.04

Xiaohai Li (haixiaolee@gamil.com)

## Introduction
My hardware platform is Intel Xeon E5-2618L 10-core processor and NVidia GTX1060 6GB graphic card. The OS distro is Ubuntu Mate 16.04.1 LTS x64.

The GTX1060 driver, Ubuntu system, GCC 5.4, torch and CUDA SDK have a compatibility problem that blocks me to use GPU acceleration for Openface.

To use GTX1060 with CUDA, you need to install CUDA8.0 SDK. Visit [NVidia web site][cuda_info] for more information:


## Preparation
Install dependence:
``` sh
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential cmake curl gfortran git libatlas-dev libavcodec-dev libavformat-dev libboost-all-dev libgtk2.0-dev libjpeg-dev liblapack-dev libswscale-dev pkg-config python-dev python-pip wget -y
```

Install python packages:
```sh
pip install numpy scipy pandas scikit-learn scikit-image  
```

Install appropriate NVidia drivers and tools for GTX1060:
```sh
sudo apt-get purge nvidia*
sudo apt-get install nvidia-367 nvidia-367-dev nvidia-opencl-icd-367 nvidia-settings
sudo apt-get install 
```

## Install OpenCV

Install dependence, some of them may be installed in previous step:
``` sh
# Required:
sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
# Optional
sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
```

Fetch OpenCV and switch to version 2.4.13:
``` sh
git clone https://github.com/opencv/opencv.git
cd opencv
git checkout 2.4.13
```

Use cmake to configure OpenCV with CUDA/OpenCL or OpenMP (multi CPU cores) support.
``` sh
mkdir build
cd build
cmake -D WITH_CUDA=1 -D WITH_OPENMP=1 -D WITH_OPENCL=1 -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
```

Compile and install OpenCV, and set -jxx according to your host PC's multi-thread capability:
``` sh
make -j20
sudo make install
```

For more information refer to the [OpenCV installation guide][opencv_ins].

## Install dlib

Fetch dlib and switch to version 18.18:
``` sh
git clone https://github.com/davisking/dlib.git
cd dlib
git checkout v19.0
```

Configure, compile and install dlib:
``` sh
cd python_examples
cmake ../tools/python  
cmake --build . --config Release -- -j20  
cp dlib.so /usr/local/lib/python2.7/dist-packages  
```

Unfortunately, dlib doesn't support GPU acceleration at all.

## Install OpenCL/CUDA enabled Torch distro:

Fetch cltorch and install dependens:
``` sh
git clone --recursive https://github.com/hughperkins/distro -b distro-cl ~/torch-cl
cd ~/torch-cl
bash install-deps
```

Because there's compatible issue between GCC4.9, boost and dlib, we should change the default gcc to GCC5.4 before installing cltorch. Edit ./install.sh and replace gcc-4.9 & g++-4.9 to gcc & g++.
``` sh
if [[ $(gcc -dumpversion | cut -d . -f 1) == 5 ]]; then {
#  export CC=gcc-4.9
#  export CXX=g++-4.9
  export CC=gcc
  export CXX=g++
} fi
...
if [[ $(gcc -dumpversion | cut -d . -f 1) == 5 ]]; then {
#  echo export CC=gcc-4.9>>$PREFIX/bin/torch-activate
#  echo export CXX=g++-4.9>>$PREFIX/bin/torch-activate
  echo export CC=gcc>>$PREFIX/bin/torch-activate
  echo export CXX=g++>>$PREFIX/bin/torch-activate
} fi
```

Then install cltorch:
``` sh
./install.sh
```

To verify OpenCL features, use these commands below:
``` sh
source ~/torch-cl/install/bin/torch-activate
luajit -l torch -e 'torch.test()'
luajit -l nn -e 'nn.test()'
luajit -l cltorch -e 'cltorch.test()'
luajit -l clnn -e 'clnn.test()'
```

The cutorch & cunn are also available:
``` sh
luajit -l cutorch -e 'cutorch.test()'
luajit -l cunn -e 'nn.testcuda()'
```

To update cltorch use the command:
``` sh
cd ~/torch-cl
git pull
git submodule update --init --recursive
./install.sh
```

## Install Openface

Before install Openface, check if OpenCV and dlib are correctly configured in Python:
``` sh
import cv2, dlib
```

Install dependent lua packages:
``` sh
luarocks install dpnn
luarocks install optim
luarocks install csvigo
luarocks install torchx
luarocks install optnet
```

Fetch and install Openface:
``` sh
git clone https://github.com/cmusatyalab/openface.git  
git submodule init  
git submodule update 
sudo python setup.py install
```

Run get-models script to download Openface and dlib trained models:
``` sh
models/get-models.sh
```

Some demos for test:
``` sh
# Face comparison demo:
./demos/compare.py images/examples/{lennon*,clapton*}
# Image classifier demo:
./demos/classifier.py infer models/openface/celeb-classifier.nn4.small2.v1.pkl ./images/examples/carell.jpg
```

To execute the web demo, install some dependence first.
``` sh
demos/web/install-deps.sh
pip install -r demo/web/requirements.txt
```

Start the web server:
``` sh
demos/web/start-servers.sh
```

Connect a USB camera to the computer, open Chrome and use the local host address to access demo server:
``` sh
http://localhost:8000
```

Enjoy your Openface time!

  [opencv_ins]: http://docs.opencv.org/2.4/doc/tutorials/introduction/linux_install/linux_install.html
  [cuda_info]: http://developer.nvidia.com/cuda-toolkit

