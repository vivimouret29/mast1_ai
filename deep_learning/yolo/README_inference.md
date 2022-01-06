## 1. Original Github
```
downlaod original weights here : https://github.com/AlexeyAB/darknet
```



## 2. Connection au container
To attach to the container (le container "darknet_training" doit être déjà en execution, controler avec la commande `docker ps`)
```bash
$(sudo) docker attach --detach-keys="ctrl-a,x" darknet_training
```
**NOTE** : In order to get out of the container without exiting it press `CTRL+A` then press `X`. It will get the user out of the running container.



## 3.a Executer l'inférence sur une image spécifique
```bash
$ ./darknet detector test <path_to_file.data> <path_to_file.cfg> <path_to_file.weights> <path_to_image.jpg> -dont_show
```
* Le fichier .data contient les infos sur les données, le.cfg contient la config du modèle (utiliser le même que celui de l'entrainement)
* Le fichier .weights contient les poids du modèle entrainé. Il devrait être dans `backup/yolo_*_best.weight`
* Par exemple, si on veut lancer le modèle preentrainé sur COCO:
```bash
$ ./darknet detector test ./cfg/coco.data ./cfg/yolov4.cfg yolov4.weights data/dog.jpg -dont_show
```
ou sur un modèle custom appris par TL:
```bash
$ ./darknet detector test ./obj.data ./yolov4-tiny-obj.cfg ./backup/yolov4-tiny-obj_best.weights data/obj/CFR_1621.jpg -dont_show
```


## 3.b Executer l'inférence sur un ensemble d'images et sauvegarder les résultats dans un fichier de texte
```bash
./darknet detector test <path_to_file.data> <path_to_file.cfg> <path_to_file.weights> -dont_show -ext_output < data/valid.txt > result.txt
```
* `results.txt` is the file where the results are stored
* `<data/train.txt>` is the path towards a .txt file containing a list of all the paths to the images on which we want to run the model
