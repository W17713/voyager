import re
import os
IPlistfile='asset\IPlist.txt'
def addIPrange(IPstring):
    IP=re.search(r'(\d*\.\d*\.\d*\.)(\d*)-(\d*)',IPstring) #[\d*]
    netsegment=IP[1]
    firstIP=IP[2]
    lastIP=IP[3]
    currentdir=os.getcwd()
    with open(os.path.join(currentdir,IPlistfile),'w+') as ipsfile:
        for i in range(int(firstIP),int(lastIP)+1):
            ipsfile.write(netsegment+str(i)+'\n')
    return 'successful'

def addIPrandom(IPlist):
    currentdir=os.getcwd()
    with open(os.path.join(currentdir,IPlistfile),'w+') as ipsfile:
        for i in range(len(IPlist)):
            ipsfile.write(i+'\n')
    return 'successful'

def getIPs():
    currentdir=os.getcwd()
    with open(os.path.join(currentdir,IPlistfile),'r') as ipsfile:
        iplist=ipsfile.readlines()
    return iplist



        

