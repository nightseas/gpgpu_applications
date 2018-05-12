## Tags

#### cuda9.1-ubuntu16.04 (=latest)

Ubuntu 16.04 + CUDA 9.1, which supports NVIDIA Volta GPUs such as V100 (not tested), and older ones.

More information: 

 - [CUDA](http://www.nvidia.com/object/cuda_home_new.html)
 - [Pytorch](https://pytorch.org)

## Requirement

- [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker) - see [requirements](https://github.com/NVIDIA/nvidia-docker/wiki/CUDA#requirements) for more details.

## Test

```sh
docker run -it --runtime=nvidia nightseas/pytorch bash
```

### 

Pytorch Basic MNIST Example

```sh
git clone https://github.com/pytorch/examples
cd examples/mnist
pip3 install -r requirements.txt

python main.py
```

### Pytorch Auto Test Results

Platform: Dual Intel E5-2699v4 + NVIDIA P100

NVIDIA Driver: 390.48

Pytorch: v0.4.0

```sh
git clone --recursive https://github.com/pytorch/pytorch
cd pytorch
git checkout v0.4.0
pip3 install -r requirements.txt

cd test
python run_test.py 

--------------------------------------

Running test_autograd ...
Ran 784 tests in 110.118s
OK

Running test_cpp_extensions ...
Ran 6 tests in 5.280s
OK

Running test_cuda ...
Ran 396 tests in 83.172s
OK (skipped=12)

Running test_dataloader ...
Ran 42 tests in 6.842s
OK (skipped=1)

Running test_distributed ...
Ran 41 tests in 42.162s
OK (skipped=22)
Ran 41 tests in 45.037s
OK (skipped=22)
Ran 41 tests in 5.408s
OK (skipped=9)
Ran 41 tests in 11.949s
OK (skipped=9)
Ran 41 tests in 120.216s
OK (skipped=31)
Ran 41 tests in 122.232s
OK (skipped=31)

Running test_distributions ...
Ran 149 tests in 12.358s
OK (skipped=44)

Running test_indexing ...
Ran 40 tests in 0.051s
OK

Running test_jit ...
Ran 142 tests in 28.509s
OK (skipped=4, expected failures=3)

Running test_legacy_nn ...
Ran 426 tests in 140.719s
OK (skipped=4)

Running test_multiprocessing ...
Ran 21 tests in 84.834s
OK (skipped=1)

Running test_nccl ...
Ran 6 tests in 17.971s
OK

Running test_nn ...
Ran 1104 tests in 1380.985s
OK (skipped=14)

Running test_optim ...
Ran 30 tests in 65.653s
OK

Running test_sparse ...
Ran 465 tests in 31.899s
OK (skipped=36)

Running test_torch ...
Ran 309 tests in 31.833s
OK (skipped=12)

Running test_utils ...
Ran 153 tests in 31.343s
OK (skipped=3)

```

## Known Issue

N/A
