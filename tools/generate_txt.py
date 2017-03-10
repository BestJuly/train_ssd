import sys    
import pdb
    
def name(s):
    l = len(s)
    #pdb.set_trace()
    if l==1:
        s = '000'+s
    if l==2:
        s = '00'+s
    if l==3:
        s = '0'+s
    return s


if __name__ == "__main__":  
  with open('trainval.txt','a+') as f:
    for i in range(413):
        if i%5!=4:
          s = str(i)
          s = name(s)
          f.write(s+"\n")
  with open('train.txt','a+') as f:
    for i in range(413):
        if i%5==0 or 1 or 2:
          s = str(i)
          s = name(s)
          f.write(s+"\n")
  with open('val.txt','a+') as f:
    for i in range(413):
        if i%5==3:
          s = str(i)
          s = name(s)
          f.write(s+"\n")
  with open('test.txt','a+') as f:
    for i in range(413):
        if i%5==4:
          s = str(i)
          s = name(s)
          f.write(s+"\n")