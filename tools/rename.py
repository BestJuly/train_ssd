# encoding: utf-8  
import os  
import os.path  
import pdb
import sys

def num2str(count):
    if count<10:
        name = '0000'+str(count)
    elif count<100:
        name = '000'+str(count)
    elif count <1000:
        name = '00'+str(count)
    elif count < 10000:
        name = '0'+ str(count)
    else:
        name = str(count)
    return name
    
curDir = sys.path[0]
count = 0
for parent, dirnames, filenames in os.walk(curDir):    
    for filename in filenames:  
        if filename != 'rename.py':
            newName = num2str(count)+'.jpg'
            print(filename, "---->", newName)  
            os.rename(os.path.join(parent, filename), os.path.join(parent, newName))  
            count = count + 1
  
print 'All done!' 
