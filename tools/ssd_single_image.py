## setup
import numpy as np
import matplotlib.pyplot as plt
import cv2
import pdb
import os
import sys
import caffe
from google.protobuf import text_format
from caffe.proto import caffe_pb2
import time

global tcost
tcost = 0

plt.rcParams['figure.figsize'] = (10, 10)
plt.rcParams['image.interpolation'] = 'nearest'
plt.rcParams['image.cmap'] = 'gray'

# Make sure that caffe is on the python path:
caffe_root = '$CAFFE_ROOT/'  # this file is expected to be in {caffe_root}/examples
os.chdir(caffe_root)
sys.path.insert(0, 'python')

caffe.set_device(0)
caffe.set_mode_gpu()

# load PASCAL VOC labels
labelmap_file = '/PATH_TO/labelmap_voc.prototxt' # your labelmap file
file = open(labelmap_file, 'r')
labelmap = caffe_pb2.LabelMap()
text_format.Merge(str(file.read()), labelmap)

def get_labelname(labelmap, labels):
    num_labels = len(labelmap.item)
    labelnames = []
    if type(labels) is not list:
        labels = [labels]
    for label in labels:
        found = False
        for i in xrange(0, num_labels):
            if label == labelmap.item[i].label:
                found = True
                labelnames.append(labelmap.item[i].display_name)
                break
        assert found == True
    return labelnames

# use nms to rectify results
def nms(top_indices, det_conf, det_xmin, det_ymin, det_xmax, det_ymax):    
    new_indices= []
    while len(top_indices) > 0:
        i = 0
        jj = -1
        for j in range (len(top_indices)-1):
            # calculate IOU
            x1 = max(det_xmin[top_indices[i]],det_xmin[top_indices[1+j]])
            y1 = max(det_ymin[top_indices[i]],det_ymin[top_indices[1+j]])
            x2 = min(det_xmax[top_indices[i]],det_xmax[top_indices[1+j]])
            y2 = min(det_ymax[top_indices[i]],det_ymax[top_indices[1+j]])
            inter = max(0, x2-x1) * max(0, y2-y1)
            s1 = (det_xmax[top_indices[i]]-det_xmin[top_indices[i]])*(det_ymax[top_indices[i]]-det_ymin[top_indices[i]])
            s2 = (det_xmax[top_indices[1+j]]-det_xmin[top_indices[1+j]])*(det_ymax[top_indices[1+j]]-det_ymin[top_indices[1+j]])
            o1 = inter / max(s1, s2)
            o2 = inter / min(s1, s2)
            # print o1,o2
            if o1 > 0.75 and o2 > 0.8:
                jj = 1+j
                break
        if jj==-1:
            new_indices.append(top_indices[i])
            top_indices.pop(i)
        elif det_conf[top_indices[i]]>det_conf[top_indices[jj]]:
            new_indices.append(top_indices[i]) 
            top_indices.pop(jj)
            top_indices.pop(i)  
        else:
            new_indices.append(top_indices[jj]) 
            top_indices.pop(jj)
            top_indices.pop(i)  
    return new_indices

def detect_obj(imname):
    global tcost
    impath = '$CAFFE_ROOT/data/mydataset/test/testpic/'+imname+'.jpg' # path to your test image
    image = caffe.io.load_image(impath)
    # image is image_data, the data form is float, transformed by dividing uint8 data by 255

    ## Run the net and examine the top_k results
    transformed_image = transformer.preprocess('data', image)
    net.blobs['data'].data[...] = transformed_image

    # Forward pass.
    ## print running time
    t0 = time.clock()
    detections = net.forward()['detection_out']
    t1 = time.clock()
    print "%f s" % (t1-t0)
    tcost = tcost + (t1 - t0)

    # Parse the outputs.
    det_label = detections[0,0,:,1]
    det_conf = detections[0,0,:,2]
    det_xmin = detections[0,0,:,3]
    det_ymin = detections[0,0,:,4]
    det_xmax = detections[0,0,:,5]
    det_ymax = detections[0,0,:,6]
    
    # Get detections with confidence higher than 0.6.
    # top_indices = [i for i, conf in enumerate(det_conf) if conf >= 0.6]

    top_indices = [i for i, label in enumerate(det_label) if det_conf[i]>=0.4]
    # nms
    top_indices = nms(top_indices, det_conf, det_xmin, det_ymin, det_xmax, det_ymax)
    top_conf = det_conf[top_indices]
    top_label_indices = det_label[top_indices].tolist()
    top_labels = get_labelname(labelmap, top_label_indices)
    top_xmin = det_xmin[top_indices]
    top_ymin = det_ymin[top_indices]
    top_xmax = det_xmax[top_indices]
    top_ymax = det_ymax[top_indices]
    
    ## Plot the boxes
    colors = plt.cm.hsv(np.linspace(0, 1, 21)).tolist()
    currentAxis = plt.gca()

    for i in xrange(top_conf.shape[0]):
        xmin = int(round(top_xmin[i] * image.shape[1]))
        ymin = int(round(top_ymin[i] * image.shape[0]))
        xmax = int(round(top_xmax[i] * image.shape[1]))
        ymax = int(round(top_ymax[i] * image.shape[0]))
        score = top_conf[i]
        label = int(top_label_indices[i])
        label_name = top_labels[i]
        #with open('$CAFFE_ROOT/data/mydataset/test/result.txt','a+') as f:
        #    f.write(imname+'.jpg'+'\t'+label_name+'\t'+str(xmin)+'\t'+str(ymin)+'\t'+str(xmax)+'\t'+str(ymax)+'\n')
        #
        display_txt = '%s: %.2f'%(label_name, score)
        coords = (xmin, ymin), xmax-xmin+1, ymax-ymin+1
        color = colors[label]
        currentAxis.add_patch(plt.Rectangle(*coords, fill=False, edgecolor=color, linewidth=4))
        currentAxis.text(xmin, ymin, display_txt, bbox={'facecolor':color, 'alpha':0.5})

    plt.imshow(image)
    savepath = '$CAFFE_ROOT/data/mydataset/test/'+imname+'.png'
    plt.savefig(savepath)
    plt.close('all')
    # plt.show()

if __name__ == '__main__':
    global tcost
    ## Load the net in the test phase for inference, and configure input preprocessing.
    model_def = '$CAFFE_ROOT/models/myssd/SSD_300x300/deploy.prototxt'
    model_weights = '$CAFFE_ROOT/models/myssd/SSD_300x300/VGG_VOC0712_SSD_300x300_iter_120000.caffemodel'

    net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

    # input preprocessing: 'data' is the name of the input blob == net.inputs[0]
    transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
    transformer.set_transpose('data', (2, 0, 1))
    transformer.set_mean('data', np.array([104,117,123])) # mean pixel
    transformer.set_raw_scale('data', 255)  # the reference model operates on images in [0,255] range instead of [0,1]
    transformer.set_channel_swap('data', (2,1,0))  # the reference model has channels in BGR order instead of RGB

    ## SSD detection
    # set net to batch size of 1
    image_resize = 300
    net.blobs['data'].reshape(1,3,image_resize,image_resize)

    imname = '00501' # in this case, detect objects in 00501.jpg
    detect_obj(imname)


