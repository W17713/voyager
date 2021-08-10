import subprocess
from subprocess import CalledProcessError 
import paramiko
import socket
import os
import platform

class Remoteserver:
    def __init__(self,host,port,username,password):
        self.host=host
        self.port=port
        self.username=username
        self.password=password
    
    def ping(self):
        try:
            output=subprocess.run('ping '+self.host,check=True)
            retcode=output.returncode
            return True,retcode
        except CalledProcessError as cpe:
            retcode=cpe.returncode
            return False,retcode
    
    def connect(self):
        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host,self.port,self.username,self.password)
            stdin,stdout,stderr=ssh.exec_command('uname -a')
            #output=subprocess.run('ssh '+username+'@'+self.host) #ps605332.dreamhostps.com
            output=stdout.readlines()  
            return True,output
        except socket.error as se:
            return False,se
        
    
    def checkftp(self):
        try:
            transport=paramiko.Transport(self.host,self.port)
            transport.connect(None,self.username,self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            curdir=os.getcwd()
            remotedir=sftp.getcwd()
            fileattributes=sftp.put(os.path.join(curdir,'asset/testfile.txt'),remotedir,None,confirm=True)
            if fileattributes.st_uid:
                sftp.remove(os.path.join(remotedir,'testfile.txt'))
            if sftp:
                sftp.close()
            if transport:
                transport.close()
            ret = True
            return ret,'successful'
        except socket.error as se:
            ret=False
            return ret,se
    
    def checkmyENV(self):
        ENV={}
        os=platform.platform()
        ENV['os']=os
        try:
            pyversion=subprocess.run('python --version')
            ENV['pyversion']=pyversion.stdout
        except CalledProcessError as cpe:
            ENV['pyversion']='n/a'
        return ENV
        
    def deployPackage():
        print('Package deploying....')

            

        



