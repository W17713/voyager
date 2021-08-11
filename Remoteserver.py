import subprocess
from subprocess import CalledProcessError 
from subprocess import SubprocessError
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
        output=subprocess.run('ping '+self.host,capture_output=True,check=True)
        try:
            output=subprocess.run('ping '+self.host,capture_output=True,check=True)
            retcode=output.returncode
            return True,retcode
        except SubprocessError as cpe:
            retcode=cpe.returncode
            return False,retcode
        return True,output
    
    def connect(self):
        try:
            ssh=paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(self.host,self.port,self.username,self.password)
            stdin,stdout,stderr=ssh.exec_command('uname -a')
            #output=subprocess.run('ssh '+username+'@'+self.host) 
            output=stdout.readlines()  
            return True,output
        except socket.error as se:
            print(se)
            return False,se
        
    
    def checkftp(self):
        try:
            transport=paramiko.Transport(self.host,self.port)
            transport.connect(None,self.username,self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            curdir=os.getcwd()
            sftp.chdir('/home/'+self.username+'/Maildir/cur')
            remotedir=sftp.getcwd()
            print('remotedir below ')
            testfilename='asset\onefile.txt'
            fileattributes=sftp.put(os.path.join(curdir,testfilename),os.path.join(remotedir,'onefile.txt'),callback=None,confirm=True)
            print(remotedir)
            if fileattributes.st_uid:
                sftp.remove(os.path.join(remotedir,'onefile.txt'))
            if sftp:
                sftp.close()
            if transport:
                transport.close()
            ret = True
            return ret,'successful'
        except socket.error as se:
            print('subprocess error')
            print(se)
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

            

        



