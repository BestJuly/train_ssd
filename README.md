# train_ssd
use single shot multibox detector(SSD) to train with your own dataset

## data preparation

### 0.rename images
1. put all your images in a folder   
2. put `rename.py` in the folder   
3. run `rename.py` and all images will be renamed, the name starts from `00000.jpg` 

### 1. make a list of your dataset    
Linux: `ls *.jpg > list.txt`   
Windows: `dir *jpg > list.txt`   

### 2. generate groundtruth    
usage of `gt_generate.m`:   
* classes.bmp is used to do labeling   
* modify the list `type` to meet your own classes   
* `filelist`/`filegt`/`path` should be modified according to your own condition
* when running the code, you just draw rectangles of the objects in each image and then click the classes to do labeling
* when you finish labeling in one image, just draw a rectangle whose width is more than 8 times of the height and the program will move to the next image 
* after labeling, your groundtruth is in `gt.txt`
* if there is something wrong when labeling, you can stop and modify the `skipnum` and run `gt_generate.m` to continue

### 3. generate xml files
1. put your `gt.txt` together with `txt2xml.py`   
2. modify all the paths in the `txt2xml.py`
3. run `txt2xml.py` and you will get all xml files in VOC2007/VOC2012 format

### 4. generate trainval.txt and other necessary txt files
`generate_txt.py` can be used to generate `trainval.txt`/`train.txt`/`val.txt`/`test.txt` if needed    
the rule to generate these txt files can be set on your own by modifying the python code

## train
Now you have all files in needed: images(.jpg)/labels(.xml)/list(.txt)

* All the following steps are operated in `SSD/caffe`
1. create a folder in `/data` to store your files
```
mkdir mydataset
```
2. copy `create_list.sh` 、`create_data.sh`、`labelmap_voc.prototxt` under `/data/VOC0712` to your own folder `/mydataset`
```
cp data/create* ./mydataset
cp data/label* ./mydataset
```
3. modify `labelmap_voc.prototxt` to define your own label   
4. put all your files in the following structure
```
-- mydataset
       | -- VOC2007
               | -- Annotations # your xml files
               | -- ImageSets   
                        | -- Layout         # trainval.txt、train.txt、val.txt、test.txt
                        | -- Main           # trainval.txt、train.txt、val.txt、test.txt
                        | -- Segmentation   # trainval.txt、train.txt、val.txt、test.txt
               | -- JPEGImages  # your image files
```
5. modify `create_list.sh`、`create_data.sh` according to your own condition and run in sequence to get lmdb files and other necessary files   

6. modify `/examples/ssd/ssd_pascal.py`
```
train_data      # lmdb file path for training 
test_data       # lmdb file path for testing
save_dir、snapshot_dir、job_dir、output_result_dir
name_size_file、label_map_file
num_classes     # your class numbers plus 1 (background)
num_test_image  # number of your test image
gpus            # which GPU you want to use
```
7. run `ssd_pascal.py` to train your model

## test
*This will be upload soon.*
