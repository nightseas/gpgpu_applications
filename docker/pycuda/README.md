## Tags

For now it's only Ubuntu 16.04 + CUDA 8.0, which supports NVidia Pascal GPU such as GTX1080/1070/1060. 

More information: 

 - [CUDA 8.0](http://www.nvidia.com/object/cuda_home_new.html)
 - [pyCUDA](https://documen.tician.de/pycuda/)

## Requirement

- [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker) - see [requirements](https://github.com/NVIDIA/nvidia-docker/wiki/CUDA#requirements) for more details.

## Test

```sh
nvidia-docker run -it nightseas/pycuda bash
```

 - [AES Encryption with CUDA](https://github.com/nightseas/gpgpu_applications/tree/master/docker/pycuda/python-pycuda)

## Known Issues

#### TBD
