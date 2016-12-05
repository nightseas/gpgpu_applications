## Test

```sh
docker run --device /dev/dri:/dev/dri nightseas/pyopencl:amdgpu-pro-16.40
```

Run the pyopencl example:

```sh
docker run --device /dev/dri  nightseas/pyopencl:amdgpu-pro-16.40 sh -c 'python /usr/share/doc/python-pyopencl-doc/examples/benchmark.py'
```
