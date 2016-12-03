docker build -t nightseas/cuda-torch -t nightseas/cuda-torch:cuda8.0-ubuntu16.04 cuda-torch/.
docker push nightseas/cuda-torch:cuda8.0-ubuntu16.04
docker push nightseas/cuda-torch

docker build -t nightseas/torch-opencv-dlib -t nightseas/torch-opencv-dlib:cv2.4.13-dlib19.0-cuda8.0-ubuntu16.04 torch_opencv_dlib/.
docker push nightseas/torch-opencv-dlib:cv2.4.13-dlib19.0-cuda8.0-ubuntu16.04
docker push nightseas/torch-opencv-dlib

docker build -t nightseas/openface openface/.
docker push nightseas/openface
