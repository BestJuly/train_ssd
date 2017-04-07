### ��עground truth
##### ���
ʹ���Լ���д��`matlab`���߽��б�ע����13��   
> *github����һ��[��ע����](https://github.com/tzutalin/labelImg )��������һ�£���ע������Խϸߣ�����ע���ٶȸо������Լ���д�ı�ע���ߡ�    

**ʹ��˵��**   
* `list.txt`����ļ������ƣ����ܰ�������·����
* `gt.txt`��¼���ɵ�`groundtruth`
* ~~`classes.bmp`Ϊ����������ɵ�ͼƬ�������עʱ���е�ѡ~~
* ���б��ʱ������ʱ�жϣ��ٴν��в���ʱ�޸Ĵ����е�`skipnum`��ֵ
1. �޸��ļ��е�·������𣬰����������~~�Ͷ�Ӧ��`classes.bmp`~~
2. ����`generate_gt.m`�ļ�����������Ϊ��ѡ��ѡȡĿ��->���ѡ�����->...->������һ��ͼƬ��ע��ɱ�־Ϊ�ڻ�ѡ��ѡȡĿ���ʱ��ѡ��Ŀ�Զ���ڸ�(8��)

### ����xml
*������xml�ļ�ʱ��`gt.txt`�����һ��ͼƬ��xml�ļ��޷����ɣ�Ŀǰ�ڴ����в�����gt.txtĩβ���һ�еİ취���н�� 

ʹ��`python`��д�Ĺ��߽���ע��`ground truth`���ͼƬ����`xml`�ļ�����Ӧ��`tool`�ļ����µ�`txt2xml.py`

### ����trainval.txt���ļ�
�����ļ������ǰ�˳�����еģ����ʹ�ü򵥵�`generate_txt.py`������Ӧ��`txt`�ļ�
������`test.txt`��`val.txt`�õ���

## ѵ��
### ׼������
#### ԭ��
1. ͼƬ(`*.jpg`)
2. ��ע(`*.xml`)
3. �ļ��б�(`trainval.txt/test.txt`)  

**����1**��ʹ��windowsϵͳ���ɵ�txt�ļ�����Ϊ`\r\n`���ҵĹ�������python����txt�ģ�ĩβֻ�����`\n`�����ļ����䵽linux����Ȼÿһ�еĽ�βΪ`\r\n`���������Ӧ����ϵͳ��ԭ��   
**�������**����linux��ʹ��vim��txt�ļ�������`:set fileformat=unix`�����漴�ɡ�[�ο�����](blog.csdn.net/zhangguangyi888/article/details/8159601)

**����2**��SSDѵ���ٶȹ���������GPU��ʹ���ʺܳ�һ��ʱ����Ϊ0%
**�������**��ʹ��`create_data.sh`׼�����ݵ�ʱ��ͼ���height��width�������úã�����׼�����ݵ�ʱ��ͽ���resize������ÿһ��ѵ��������ʱ��lmdb����resize�ٽ�������

#### ����һ���滻ԭ��VOC2007����
VOC�����ݴ����ʽ����
```
-- VOCdevkit
       | -- VOC2007
               | -- Annotations # ���xml�ļ�
               | -- ImageSets   # ������ݼ�����trainval.txt��test.txt��
               | -- JPEGImages  # ���ͼ���ļ�
```
���Լ���xml��txt��jpg�ļ��ŵ�ָ�����ļ���������滻���ٸ���ʵ���������`$CAFFE_ROOT/data/VOC0712`�µ�`labelmap_voc.prototxt`�����޸ġ�����ʵ�ʵ��ļ�·���޸�`create_list.sh`��`create_data.sh`�󣬰�˳���������нű��ļ��������ڶ�Ӧ·���µõ�lmdb�ļ���   
�༭`$CAFFE_ROOT/examples/ssd/ssd_pascal.py`�����ջ����������޸Ĳ������ɡ���Ҫ�޸ĵĲ������£�
```
train_data      ѵ���õ�lmdb�ļ���λ��
test_data       �����õĵ�lmdb�ļ���λ��
save_dir��snapshot_dir��job_dir��output_result_dir·��
name_size_file��label_map_file·��
num_classes     �޸�Ϊ1 + �����
num_test_image  ���Լ�ͼƬ��Ŀ
gpus            ָ��ѵ���õ�GPU��id�ţ��ö��ŷָ�
```

#### ������
> �ο����ϣ�[SSD��װѵ���Լ������ݼ�](blog.csdn.net/zhang_shuai12/article/details/52346878)   

1. ��`/data`Ŀ¼�´���һ���Լ����ļ���   
```
mkdir mydataset
```
2. ��`/data/VOC0712`Ŀ¼�µ�`create_list.sh` ��`create_data.sh`��`labelmap_voc.prototxt`�������ļ�������`/mydataset`�� 
```
cp data/create* ./mydataset
cp data/label* ./mydataset
```
3. �޸�`labelmap_voc.prototxt`, ���ļ�����label   
4. ��`/data/VOCdevkit`Ŀ¼�´���mydataset, �������Լ������ݼ����ļ��еĽṹ����
```
-- mydataset
       | -- VOC2007
               | -- Annotations # ���xml�ļ�
               | -- ImageSets   
                        | -- Layout         # ���trainval.txt��train.txt��val.txt��test.txt
                        | -- Main           # ���trainval.txt��train.txt��val.txt��test.txt
                        | -- Segmentation   # ���trainval.txt��train.txt��val.txt��test.txt
               | -- JPEGImages  # ���ͼ���ļ�
```
5. ��`/examples`�´���mydataset�ļ��У��ļ�������������ɵ�lmdb�ļ�
```
mkdir mydataset
```
6. �ļ��д����ú� ��ʼ����lmdb�ļ�, �ڴ���֮ǰ��Ҫ�޸����·��
```
./data/mydataset/create_list.sh
./data/mydataset/create_data.sh
```
7. �޸�`/examples/ssd/ssd_pascal.py`
```
train_data      ѵ���õ�lmdb�ļ���λ��
test_data       �����õĵ�lmdb�ļ���λ��
save_dir��snapshot_dir��job_dir��output_result_dir·��
name_size_file��label_map_file·��
num_classes     �޸�Ϊ1 + �����
num_test_image  ���Լ�ͼƬ��Ŀ
gpus            ָ��ѵ���õ�GPU��id�ţ��ö��ŷָ�
```
8. ����`ssd_pascal.py`����ѵ��

## ����
����ʹ��ԭ���ߴ������`ssd_detect.ipynb`���м�⡣   
Ҳ����ʹ�������ṩ��`ssd_single_image.py`�Ե���ͼƬ���м�⣬ʹ��ʱ�뽫��Ӧ��·�������޸ġ�   
![Result](https://github.com/BestJuly/train_ssd/blob/master/tools/00501.png)
