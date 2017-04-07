### 标注ground truth
##### 类别
使用自己编写的`matlab`工具进行标注，共13类   
> *github上有一个[标注工具](https://github.com/tzutalin/labelImg )，尝试了一下，标注的灵活性较高，但标注的速度感觉不如自己编写的标注工具。    

**使用说明**   
* `list.txt`存放文件的名称（可能包含部分路径）
* `gt.txt`记录生成的`groundtruth`
* ~~`classes.bmp`为根据类别生成的图片，方便标注时进行点选~~
* 进行标记时可以随时中断，再次进行操作时修改代码中的`skipnum`数值
1. 修改文件中的路径和类别，包含类别数量~~和对应的`classes.bmp`~~
2. 运行`generate_gt.m`文件，操作过程为画选框选取目标->点击选择类别->...->结束，一张图片标注完成标志为在画选框选取目标的时候，选框的宽远大于高(8倍)

### 生成xml
*在生成xml文件时，`gt.txt`的最后一张图片的xml文件无法生成，目前在代码中采用在gt.txt末尾添加一行的办法进行解决 

使用`python`编写的工具将标注的`ground truth`结合图片生成`xml`文件，对应与`tool`文件夹下的`txt2xml.py`

### 生成trainval.txt等文件
由于文件名称是按顺序排列的，因此使用简单的`generate_txt.py`生成相应的`txt`文件
在这里`test.txt`用`val.txt`得到。

## 训练
### 准备数据
#### 原料
1. 图片(`*.jpg`)
2. 标注(`*.xml`)
3. 文件列表(`trainval.txt/test.txt`)  

**问题1**：使用windows系统生成的txt文件换行为`\r\n`，我的工具是用python生成txt的，末尾只添加了`\n`但是文件传输到linux上依然每一行的结尾为`\r\n`，所以这个应该是系统的原因。   
**解决方法**：在linux下使用vim打开txt文件，输入`:set fileformat=unix`，保存即可。[参考资料](blog.csdn.net/zhangguangyi888/article/details/8159601)

**问题2**：SSD训练速度过慢，并且GPU的使用率很长一段时间内为0%
**解决方法**：使用`create_data.sh`准备数据的时候图像的height、width参数设置好，即在准备数据的时候就进行resize而不是每一轮训练迭代的时候lmdb数据resize再进入网络

#### 方案一：替换原生VOC2007数据
VOC的数据存放形式如下
```
-- VOCdevkit
       | -- VOC2007
               | -- Annotations # 存放xml文件
               | -- ImageSets   # 存放数据集，及trainval.txt、test.txt等
               | -- JPEGImages  # 存放图像文件
```
将自己的xml、txt、jpg文件放到指定的文件夹里进行替换，再根据实际情况，对`$CAFFE_ROOT/data/VOC0712`下的`labelmap_voc.prototxt`进行修改。根据实际的文件路径修改`create_list.sh`、`create_data.sh`后，按顺序依次运行脚本文件，即可在对应路径下得到lmdb文件。   
编辑`$CAFFE_ROOT/examples/ssd/ssd_pascal.py`，按照机器的配置修改参数即可。需要修改的参数如下：
```
train_data      训练用的lmdb文件的位置
test_data       测试用的的lmdb文件的位置
save_dir、snapshot_dir、job_dir、output_result_dir路径
name_size_file、label_map_file路径
num_classes     修改为1 + 类别数
num_test_image  测试集图片数目
gpus            指定训练用的GPU的id号，用逗号分隔
```

#### 方案二
> 参考资料：[SSD安装训练自己的数据集](blog.csdn.net/zhang_shuai12/article/details/52346878)   

1. 在`/data`目录下创建一个自己的文件夹   
```
mkdir mydataset
```
2. 把`/data/VOC0712`目录下的`create_list.sh` 、`create_data.sh`、`labelmap_voc.prototxt`这三个文件拷贝到`/mydataset`下 
```
cp data/create* ./mydataset
cp data/label* ./mydataset
```
3. 修改`labelmap_voc.prototxt`, 此文件定义label   
4. 在`/data/VOCdevkit`目录下创建mydataset, 并放入自己的数据集。文件夹的结构如下
```
-- mydataset
       | -- VOC2007
               | -- Annotations # 存放xml文件
               | -- ImageSets   
                        | -- Layout         # 存放trainval.txt、train.txt、val.txt、test.txt
                        | -- Main           # 存放trainval.txt、train.txt、val.txt、test.txt
                        | -- Segmentation   # 存放trainval.txt、train.txt、val.txt、test.txt
               | -- JPEGImages  # 存放图像文件
```
5. 在`/examples`下创建mydataset文件夹，文件夹用来存放生成的lmdb文件
```
mkdir mydataset
```
6. 文件夹创建好后， 开始生成lmdb文件, 在创建之前需要修改相关路径
```
./data/mydataset/create_list.sh
./data/mydataset/create_data.sh
```
7. 修改`/examples/ssd/ssd_pascal.py`
```
train_data      训练用的lmdb文件的位置
test_data       测试用的的lmdb文件的位置
save_dir、snapshot_dir、job_dir、output_result_dir路径
name_size_file、label_map_file路径
num_classes     修改为1 + 类别数
num_test_image  测试集图片数目
gpus            指定训练用的GPU的id号，用逗号分隔
```
8. 运行`ssd_pascal.py`进行训练

## 测试
可以使用原作者代码里的`ssd_detect.ipynb`进行检测。   
也可以使用这里提供的`ssd_single_image.py`对单张图片进行检测，使用时请将对应的路径进行修改。   
![Result](https://github.com/BestJuly/train_ssd/blob/master/tools/00501.png)
