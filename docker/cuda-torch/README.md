## Tags

#### cuda8.0-ubuntu16.04 (=latest)
For now it's only Ubuntu 16.04 + CUDA 8.0, which supports NVidia Pascal GPU such as GTX1080/1070/1060. 

More information: 

 - [CUDA 8.0](http://www.nvidia.com/object/cuda_home_new.html)
 - [cuDNN v5](https://developer.nvidia.com/cuDNN)

## Requirement

- [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker) - see [requirements](https://github.com/NVIDIA/nvidia-docker/wiki/CUDA#requirements) for more details.



## Test

```sh
nvidia-docker run -it nightseas/cuda-torch bash
luajit -l torch -e 'torch.test()'
luajit -l nn -e 'nn.test()'

luajit -l cutorch -e 'cutorch.test()'
luajit -l cunn -e 'nn.testcuda()'
```


## Known Issues

 - Some random failures in cutorch unit test. Refer to Google group of Torch7 for more information:

https://groups.google.com/forum/m/#!msg/torch7/pgfMUUy9wWo/Mk8iGHTSAgAJ

```
Completed 105699 asserts in 169 tests with 2 failures and 0 errors
--------------------------------------------------------------------------------
bernoulli
mean is not equal to p
ALMOST_EQ failed: 0.875 ~= 0.7456697744783 with tolerance=0.1
	/root/torch/install/share/lua/5.1/cutorch/test.lua:2661: in function 'v'
	/root/torch/install/share/lua/5.1/cutorch/test.lua:3965: in function </root/torch/install/share/lua/5.1/cutorch/test.lua:3963>
--------------------------------------------------------------------------------
multinomial_without_replacement
sampled an index twice
BOOL violation condition=false
	/root/torch/install/share/lua/5.1/cutorch/test.lua:2861: in function 'v'
	/root/torch/install/share/lua/5.1/cutorch/test.lua:3965: in function </root/torch/install/share/lua/5.1/cutorch/test.lua:3963>
--------------------------------------------------------------------------------
luajit: /root/torch/install/share/lua/5.1/torch/Tester.lua:361: An error was found while running tests!
stack traceback:
	[C]: in function 'assert'
	/root/torch/install/share/lua/5.1/torch/Tester.lua:361: in function 'run'
	/root/torch/install/share/lua/5.1/cutorch/test.lua:3984: in function 'test'
	(command line):1: in main chunk
	[C]: at 0x00405d50

```



 - In cunn unit test there are errors on 2 cases which are remain to be analyzed:

(It looks like a bug, I've got a GTX1060 6GB card and running the test only took 4GB memory. But the test still falied with 'out of memory')

```
160/169 VolumetricDilatedMaxPooling_backward_batch ...................... [ERROR]
161/169 SpatialReplicationPadding_forward ............................... [ERROR]
...
Completed 1902 asserts in 169 tests with 0 failures and 2 errors
--------------------------------------------------------------------------------
VolumetricDilatedMaxPooling_backward_batch
 Function call failed
/root/torch/install/share/lua/5.1/cunn/test.lua:70: cuda runtime error (2) : out of memory at /tmp/luarocks_cutorch-scm-1-4846/cutorch/lib/THC/generic/THCStorage.cu:65
stack traceback:
	[C]: in function 'resize'
	/root/torch/install/share/lua/5.1/cunn/test.lua:70: in function 'makeNonContiguous'
	/root/torch/install/share/lua/5.1/cunn/test.lua:4552: in function 'v'
	/root/torch/install/share/lua/5.1/cunn/test.lua:5671: in function </root/torch/install/share/lua/5.1/cunn/test.lua:5669>
	[C]: in function 'xpcall'
	/root/torch/install/share/lua/5.1/torch/Tester.lua:477: in function '_pcall'
	/root/torch/install/share/lua/5.1/torch/Tester.lua:436: in function '_run'
	/root/torch/install/share/lua/5.1/torch/Tester.lua:355: in function 'run'
	/root/torch/install/share/lua/5.1/cunn/test.lua:5692: in function 'testcuda'
	(command line):1: in main chunk
	[C]: at 0x00405d50

--------------------------------------------------------------------------------
SpatialReplicationPadding_forward
 Function call failed
/root/torch/install/share/lua/5.1/cunn/test.lua:78: cuda runtime error (2) : out of memory at /tmp/luarocks_cutorch-scm-1-4846/cutorch/lib/THC/THCTensorCopy.cu:204
stack traceback:
	[C]: in function 'copy'
	/root/torch/install/share/lua/5.1/cunn/test.lua:78: in function 'makeNonContiguous'
	/root/torch/install/share/lua/5.1/cunn/test.lua:5315: in function 'v'
	/root/torch/install/share/lua/5.1/cunn/test.lua:5671: in function </root/torch/install/share/lua/5.1/cunn/test.lua:5669>
	[C]: in function 'xpcall'
	/root/torch/install/share/lua/5.1/torch/Tester.lua:477: in function '_pcall'
	/root/torch/install/share/lua/5.1/torch/Tester.lua:436: in function '_run'
	/root/torch/install/share/lua/5.1/torch/Tester.lua:355: in function 'run'
	/root/torch/install/share/lua/5.1/cunn/test.lua:5692: in function 'testcuda'
	(command line):1: in main chunk
	[C]: at 0x00405d50

--------------------------------------------------------------------------------
luajit: /root/torch/install/share/lua/5.1/torch/Tester.lua:363: An error was found while running tests!
stack traceback:
	[C]: in function 'assert'
	/root/torch/install/share/lua/5.1/torch/Tester.lua:363: in function 'run'
	/root/torch/install/share/lua/5.1/cunn/test.lua:5692: in function 'testcuda'
	(command line):1: in main chunk
	[C]: at 0x00405d50
```
