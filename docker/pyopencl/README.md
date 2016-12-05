## Tags

#### latest
This is only a base image without any drivers.

#### nvidia-367
Nvidia 367.57 driver integrated, which supports NVidia Pascal GPU such as GTX1080/1070/1060. 

#### amdgpu-pro-16.40
AMD GPU Pro 16.40-348864 driver integrated, which supports AMD Polaris GPU such as RX480/470.

More information: 

TBD.

## Requirement

 - You should choose the exactly same version of driver running on both container and host.

## Test

```sh
# Nvidia (change /dev/nvidia0 to your GPU)
docker run --device /dev/nvidiactl --device /dev/nvidia0  --device /dev/nvidia-uvm -it nightseas/pyopencl:nvidia-367

# AMD
docker run --device /dev/dri nightseas/pyopencl:amdgpu-pro-16.40
```

