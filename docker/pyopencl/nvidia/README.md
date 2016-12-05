## Test

```sh
docker run --device /dev/nvidiactl --device /dev/nvidia0  --device /dev/nvidia-uvm nightseas/pyopencl:nvidia-367
```

Run the pyopencl example:

```sh
docker run --device /dev/nvidiactl --device /dev/nvidia0  --device /dev/nvidia-uvm nightseas/pyopencl:nvidia-367 sh -c 'python /usr/share/doc/python-pyopencl-doc/examples/benchmark.py'
```
