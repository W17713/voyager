import re
import os
IPlistfile='asset\IPlistfile.txt'
def addIPrange(IPstring):
    IP=re.search(r'(\d*\.\d*\.\d*\.)(\d*)-(\d*)',IPstring) #[\d*]
    netsegment=IP[1]
    firstIP=IP[2]
    lastIP=IP[3]
    currentdir=os.getcwd()
    with open(os.path.join(currentdir,IPlistfile),'w+') as ipsfile:
        for i in range(int(firstIP),int(lastIP)+1):
            ipsfile.write(netsegment+str(i)+'\n')

def addIPrandom(IPlist):
    with open(os.path.join(currentdir,IPlistfile),'w+') as ipsfile:
        for i in range(len(IPlist)):
            ipsfile.write(i+'\n')



        

