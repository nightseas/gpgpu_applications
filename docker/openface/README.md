## Tags

For now it's only Ubuntu 16.04 + CUDA 8.0, which supports NVidia Pascal GPU such as GTX1080/1070/1060. 

More information: 

 - [CUDA 8.0](http://www.nvidia.com/object/cuda_home_new.html)
 - [cuDNN v5](https://developer.nvidia.com/cuDNN)
 - [CMU openface](http://cmusatyalab.github.io/openface/)

## Requirement

- [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker) - see [requirements](https://github.com/NVIDIA/nvidia-docker/wiki/CUDA#requirements) for more details.



## Test

Face comparison demo:

```sh
/root/openface/demos/compare.py images/examples/{lennon*,clapton*}
```

Image classifier demo:

```sh
/root/openface/demos/classifier.py infer models/openface/celeb-classifier.nn4.small2.v1.pkl ./images/examples/carell.jpg
```

Real-time web based face recognition:

```sh
/root/openface/demos/web/start-servers.sh
```

## Known Issues

Some function may not work well:

```
root:~/openface# ./run-tests.sh 
ttests.openface_api_tests.test_pipeline ... ok
tests.openface_batch_represent_tests.test_batch_represent ... ok
tests.openface_demo_tests.test_compare_demo ... ok
tests.openface_demo_tests.test_classification_demo_pretrained ... ok
tests.openface_demo_tests.test_classification_demo_pretrained_multi ... ok
tests.openface_demo_tests.test_classification_demo_training ... ok
tests.openface_neural_net_training_tests.test_dnn_training ... FAIL

======================================================================
FAIL: tests.openface_neural_net_training_tests.test_dnn_training
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/usr/lib/python2.7/dist-packages/nose/case.py", line 197, in runTest
    self.test(*self.arg)
  File "/root/openface/tests/openface_neural_net_training_tests.py", line 82, in test_dnn_training
    assert np.mean(trainLoss) < 0.3
AssertionError: 
...
```
