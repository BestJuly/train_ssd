#encoding:utf-8
'''
transform txt to xml in VOC2007 form
data file is in output.txt, each line forms like name,xmin,ymin,xmax,ymax,class
one line only has one object
if an image has seceral objects, those information comes together in [filename]
'''
from xml.dom.minidom import Document
import pdb
from PIL import Image
# import Image

def add_element(doc, root, name, text):
    index_name = doc.createElement(name)
    index_text = doc.createTextNode(text)
    index_name.appendChild(index_text)
    root.appendChild(index_name)

def add_object(doc, type, xmin, ymin, xmax, ymax):
    object = doc.createElement('object')
    annotation.appendChild(object)
    add_element(doc, object, 'name', type)
    add_element(doc, object, 'pose', 'Unspecified')
    add_element(doc, object, 'truncated', '0')
    add_element(doc, object, 'difficult', '0')
    bndbox = doc.createElement('bndbox')
    object.appendChild(bndbox)
    if xmin == 0:
        xmin = 1
    if ymin == 0:
        ymin = 1
    add_element(doc, bndbox, 'xmin', str(xmin))
    add_element(doc, bndbox, 'ymin', str(ymin))
    add_element(doc, bndbox, 'xmax', str(xmax))
    add_element(doc, bndbox, 'ymax', str(ymax))


if __name__ == '__main__':
    #pre setting
    prename = 'prename.jpg'
    doc = Document()
    
    filename = ('gt.txt')
    txt = open(filename)
    split_line = txt.readline().strip().split(',')
    while (split_line):
        # pdb.set_trace()
        if len(split_line) == 1:
            break
        picname = split_line[0]
        if picname == 'XXXXX.jpg':
            break;
        xmin = split_line[1]
        ymin = split_line[2]
        xmax = split_line[3]
        ymax = split_line[4]
        type = split_line[5]
        if picname==prename:
            add_object(doc, type, xmin, ymin, xmax, ymax)
        else:
        #write result and go to next image
            picnum = prename.split('.')
            outname = 'xml/'+picnum[0]+'.xml'
            f = open(outname,'w')
            f.write(doc.toprettyxml(indent = '\t'))
            f.close()

            doc = Document()#reset
            prename = picname#reset name
            annotation = doc.createElement('annotation')
            doc.appendChild(annotation)

            add_element(doc, annotation, 'folder', 'VOC2007')
            add_element(doc, annotation, 'filename', picname)

            source = doc.createElement('source')
            annotation.appendChild(source)
            add_element(doc, source, 'database', 'Staff Database')
            add_element(doc, source, 'annotation', 'VOC2007')
            add_element(doc, source, 'image', 'flickr')
            add_element(doc, source, 'flickrid', 'NULL')

            owner = doc.createElement('owner')
            annotation.appendChild(owner)
            add_element(doc, owner, 'flickrid', 'NULL')    
            add_element(doc, owner, 'name', 'BestJuly')
            #read from picture
            picpath = picname
            im = Image.open(picpath)
            imsize = im.size
            width = imsize[0]
            height = imsize[1]
            depth = 3
            del im,imsize
            size = doc.createElement('size')
            annotation.appendChild(size)
            add_element(doc, size, 'width', str(width))  
            add_element(doc, size, 'height', str(height))
            add_element(doc, size, 'depth', str(depth))

            add_element(doc, annotation, 'segmented', '0')
            add_object(doc, type, xmin, ymin, xmax, ymax)
        split_line = txt.readline().strip().split(',')

    picnum = prename.split('.')
    outname = 'xml/'+picnum[0]+'.xml'
    f = open(outname,'w')
    f.write(doc.toprettyxml(indent = '\t'))
    f.close()