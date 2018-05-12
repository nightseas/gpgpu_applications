## Tags

#### cuda9.1-ubuntu16.04 (=latest)

Ubuntu 16.04 + CUDA 9.1, which has been verified on NVidia P100.

#### cuda8.0-ubuntu16.04

Ubuntu 16.04 + CUDA 8.0, which supports NVidia Pascal GPU such as GTX1080/1070/1060. 

More information: 

 - [CUDA](http://www.nvidia.com/object/cuda_home_new.html)
 - [FFmpeg with CUDA](https://developer.nvidia.com/ffmpeg)

## Requirement

- [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker) - see [requirements](https://github.com/NVIDIA/nvidia-docker/wiki/CUDA#requirements) for more details.
- [NVIDIA Driver Version Requirements from NV Codec Headers](https://github.com/FFmpeg/nv-codec-headers).

## Test

```sh
docker run -it --runtime=nvidia --volume path_to_your_data:/root/data nightseas/ffmpeg bash
```

### Decode a single H.264 to YUV

To decode a single H.264 encoded elementary bitstream file into YUV, use the following command:

```sh
ffmpeg -vsync 0 -c:v h264_cuvid -i <input.mp4> -f rawvideo <output.yuv>
```

### Encode a single YUV file to a bitstream

To encode a single YUV file into an H.264/HEVC bitstream, use the following command:

```sh
# H264
ffmpeg -f rawvideo -s:v 1920x1080 -r 30 -pix_fmt yuv420p -i <input.yuv> -c:v h264_nvenc -preset slow -cq 10 -bf 2 -g 150 <output.mp4>
# H265/HEVC (No B-frames)
ffmpeg -f rawvideo -s:v 1920x1080 -r 30 -pix_fmt yuv420p -i <input.yuv> -vcodec hevc_nvenc -preset slow -cq 10 -g 150 <output.mp4>
```

### Transcode a single video file to N streams

Note: For GTX10xx GPU, only TWO encoders are available at the same time, although the encoder usage are not 100%. Acctually in my case, transcoding 2 1080p H264 videos only use 30% of encoder resouces on GTX1080. It seems like a software limitation set by NVIDIA. And there's no such limitation on P100.

To do 1:N transcode, use the following command:

```sh
ffmpeg -hwaccel cuvid -c:v h264_cuvid -i <input.mp4> -vf scale_npp=1280:720 -vcodec h264_nvenc <output0.mp4> -vf scale_npp=640:480 -vcodec h264_nvenc <output1.mp4>
```

### Perf Test

Platform: Dual Intel E5-2699v4 + NVIDIA P100

NVIDIA Driver: 390.48

FFmpeg 4.0 + CUDA9.1


```sh
ffmpeg -hwaccel cuvid -c:v h264_cuvid -i big_buck_bunny_1080p_H264_AAC_25fps_7200K.MP4 -vf scale_npp=1280:720 -vcodec h264_nvenc output0.mp4 -vf scale_npp=640:480 -vcodec h264_nvenc output1.mp4

...

frame= 1130 fps=258 q=23.0 Lq=19.0 size=   12277kB time=00:00:45.16 bitrate=2227.1kbits/s dup=10 drop=0 speed=10.3x    
video:22926kB audio:1412kB subtitle:0kB other streams:0kB global headers:0kB muxing overhead: unknown
[aac @ 0x2204080] Qavg: 828.371
[aac @ 0x22aa4c0] Qavg: 828.371
```


## Known Issue

N/A
