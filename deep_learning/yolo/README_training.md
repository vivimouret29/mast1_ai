## 1. Original Github
```
downlaod original weights here : https://github.com/AlexeyAB/darknet
```

## 2. Preparer données et cfg files sur la machine host (Scalio)
1. Put all your dataset (custom ".jpg" and ".txt" annotations) on this folder : `/dataset/data/obj`
2. Split train and validation data : Generate the **val.txt** and **train.txt** on the `/dataset/data` folder 
``` bash
$ cd dataset
$ python train_test_split.py
```
3. Please change the **yolo-obj.cfg**, **obj.data** and **yolo-obj.names** file according to your custom class numbers and ***YOLOv4***
4. The full **dataset** direcotry structures should look like below
```bash
├── data
│   ├── obj
│   │   ├── 000000000036.jpg
│   │   ├── 000000000036.txt
│   │   ├── 000000581921.jpg
│   │   ├── 000000581921.txt
│   │   └── ................
│   ├── train.txt
│   ├── val.txt
│   └── yolo-obj.names
├── obj.data
├── train_test_split.py
└── yolo-obj.cfg
```

## 3. Training
### 3.1. If you have a running darknet_yolo docker container
#### 3.1.1. Attach to the container
```bash
$ docker attach --detach-keys="ctrl-a,x" darknet_training
```
In order to get out of the container without exiting it **press** `CTRL+A` then **press** `X`. It will get the user out of the running container.

#### 3.1.2. Train a YOLOv4 model
Inside the running container (/darknet#), run:
```bash
./darknet detector train <path_to_file.data> <path_to_file.cfg> <pretrained_model> -map -dont_show
```
* le fichier .data contient les infos sur les données, le.cfg contient la config du modèle (utiliser le même que celui de l'entrainement)
* le fichier <pretrained_model> contient le modèle pre-entrainé de départ pour faire du transfer learning. Pour le défault yolov4, utiliser yolov4.conv.137 
* par exemple: ./darknet detector train obj.data yolo-obj.cfg yolov4.conv.137 -map -dont_show



### 3.2. If you don't have a darknet_yolo docker container running
Run the following commands to start container
#### 3.2.1 Build the container (if not built before)
à l'emplacement du dockerfile, executer : 
```bash
$ docker build -t docker-darknet_yolo:latest .
```
#### 3.2.2 Running the container in detached mode:
```bash
sudo docker run -it --name darknet_training -d \
  -v /home/daftvm/workspace/mast1_ai/deep_learning/yolo/training:/darknet \
  daisukekobayashi/darknet:yolov4-cpu-cv-ubuntu20.04

  darknet detector train obj.data yolov4-tiny.cfg yolov4-tiny.weights -map -dont_show
  # -v ${pwd}data/val.txt:/darknet/data/val.txt \
  # -v ${pwd}data/train.txt:/darknet/data/train.txt \
  # -v ${pwd}data/yolo-obj.names:/darknet/data/yolo-obj.names \
  # -v ${pwd}obj.data:/darknet/obj.data \
  # -v ${pwd}yolo-obj.cfg:/darknet/yolov4-tiny.cfg \
  # -v ${pwd}backup:/darknet/backup \
```
* the last line also runs the training of the model
* replace (pwd) with your directory where you have the dataset folder (on Scalio), in order to mount it as a volume to the docker.
* the weights of the trained model will also be available in the "backup" folder, that well be mounted as a volume to the container  
* **Note** : you can change the name of the container
* **Note** : you can also run the container without running the training, attach to the container and then run the training (probably the best option)

par exemple, pour lancer l'entrainement d'un yolo-tiny
```bash
sudo docker run -it --gpus all --shm-size=1g --name darknet_training_tiny -d\
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/data/obj:/darknet/data/obj \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/data/val.txt:/darknet/data/val.txt \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/data/train.txt:/darknet/data/train.txt \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/data/yolo-obj.names:/darknet/data/yolo-obj.names \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/obj.data:/darknet/obj.data \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/yolov4-tiny-obj.cfg:/darknet/yolov4-tiny-obj.cfg \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/backup_tiny:/darknet/backup_tiny \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/yolov4-tiny.conv.29:/darknet/yolov4-tiny.conv.29 \
  docker-darknet_yolo:latest ./darknet detector train obj.data yolov4-tiny-obj.cfg yolov4-tiny.conv.29 -map -dont_show
```
* `--shm-size=1g` est parfois nécessaire sur scali opour éviter des problèmes de mémoire CUDA

```bash
sudo docker run -it --gpus all --shm-size=1g --name darknet_training -d\
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/data/obj:/darknet/data/obj \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/data/val.txt:/darknet/data/val.txt \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/data/train.txt:/darknet/data/train.txt \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/data/yolo-obj.names:/darknet/data/yolo-obj.names \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/obj.data:/darknet/obj.data \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/yolo-obj.cfg:/darknet/yolo-obj.cfg \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/yolov4-custom.cfg:/darknet/yolov4-custom.cfg \
  -v /home/administrateur/yolo4_training/docker-darknet-yolov3-yolov4-training-test/dataset/backup:/darknet/backup \
  docker-darknet_yolo:latest 

./darknet detector train obj.data yolov4-tiny-obj.cfg yolov4-tiny.conv.29 -map -dont_show
```