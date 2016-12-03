## Tags

#### cuda8.0-ubuntu16.04 (=latest)
For now it's only Ubuntu 16.04 + CUDA 8.0, which supports NVidia Pascal GPU such as GTX1080/1070/1060. 

More information: 

 - [CUDA 8.0](http://www.nvidia.com/object/cuda_home_new.html)

## Requirement

- [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker) - see [requirements](https://github.com/NVIDIA/nvidia-docker/wiki/CUDA#requirements) for more details.



## Test

```sh
nvidia-docker run -it nightseas/opencl-torch bash
luajit -l torch -e 'torch.test()'
luajit -l nn -e 'nn.test()'

luajit -l cltorch -e 'cltorch.test()'
luajit -l clnn -e 'clnn.test()'
```


## Known Issues

 - cutorch and cunn are not supported.
