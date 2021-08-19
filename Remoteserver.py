import subprocess
from subprocess import CalledProcessError 
from subprocess import SubprocessError
import paramiko
import socket
import os
import platform
from Package import Pkg as pkg2deploy

class Remoteserver:
    def __init__(self,host,port,username,password):
        self.host=host
        self.port=port
        self.username=username
        self.password=password
    
    def ping(self):
        #output=subprocess.run('ping '+self.host,capture_output=True,check=True)
        try:
            output=subprocess.run('ping '+self.host,capture_output=True,check=True)
            retcode=output.returncode
            return True,retcode
        except SubprocessError as cpe:
            retcode=cpe.returncode
            return False,retcode
        return True,output
    
    def connectssh(self):
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        return ssh       

    
    def runcommand(self,cmd='uname -a'):
        try:
            ssh=self.connectssh()
            ssh.connect(self.host,self.port,self.username,self.password)
            stdin,stdout,stderr=ssh.exec_command(cmd)
            output=stdout.readlines()
            return True,output
        except Exception as se:
            print(se)
            return False,se
        

    
    def connectsftp(self):
        transport=paramiko.Transport(self.host,self.port)
        transport.connect(None,self.username,self.password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        return transport,sftp
        
    
    def sftpcheck(self):
        try:
            transport,sftp=self.connectsftp()
            curdir=os.getcwd()
            sftp.chdir('/home/'+self.username+'/Maildir/cur')
            remotedir=sftp.getcwd()
            print('remotedir below ')
            testfilename='asset\onefile.txt'
            fileattributes=sftp.put(os.path.join(curdir,testfilename),remotedir+'/onefile.txt')
            print(remotedir)
            if fileattributes.st_uid:
                sftp.remove(remotedir+'/onefile.txt')
            if sftp:
                sftp.close()
            if transport:
                transport.close()
            return True,'successful'
        except Exception as se:
            print('subprocess error')
            print(se)
            return False,se


    def checkmyENV(self):
        ENV={}
        checks={'pyversion':'python --version','d2uversion':'dos2unix --version','bashversion':'bash --version'}
        os=platform.platform()
        ENV['os']=os
        try:
            for i,j in checks.items():
                stin,stout,sterr=self.runcommand(j)
                ENV[i]=stout
        except CalledProcessError as cpe:
            ENV['pyversion']='n/a'
        return ENV
        
    def deployPackage(self,sourcedir):
        #transfer package from local machine to remote machine
        transport,sftp=self.connectsftp()
        curdir=os.getcwd()
        loadscriptpath='script/loaderscript.sh'
        scriptpath=os.path.join(curdir,loadscriptpath)
        script=pkg2deploy(scriptpath)
        scriptattr=script.getprops()
        pkgdir=os.path.join('pkg',sourcedir)
        print('pkg dir '+pkgdir)
        dir=os.path.join(curdir,pkgdir)
        pkgs=os.listdir(dir)
        print(pkgs)
        pkglist=[]
        for p in pkgs:
            path=os.path.join(dir,p)
            pkg2d=pkg2deploy(path)
            pkg=pkg2d.getprops()
            pkglist.append(pkg)
        
        #pkgpath=os.path.join(curdir,pkgdir)
        sftp.chdir('/home/'+self.username)
        remotedir=sftp.getcwd()
        rmloadfile=remotedir+'/loaderscript.sh'
        #upload package and helper scripts to remote machine 
        try:
            sftp.put(scriptattr['path'],rmloadfile)
        except Exception as sftpexp:
            print(sftpexp)
        loadscriptsize=sftp.lstat(rmloadfile).st_size
        print(loadscriptsize)
        if scriptattr['size'] == loadscriptsize:
            #change to multithreading later
            for pkg in pkglist:
                try:
                    pkgattributes=sftp.put(pkg['path'],remotedir+'/'+pkg['name'])
                except Exception as sftpexp:
                    print(sftpexp)
            #ssh to remote machine to run scripts
            operationlist=['chmod +x '+rmloadfile,'cd '+remotedir+';sh loaderscript.sh']
            for op in operationlist:
                print(op)
                status,stout=self.runcommand(op)
                print(stout)
        if sftp:
            sftp.close()
        if transport:
            sftp.close()
        
        #if pkgattributes.st_size == pkg['size']: #size of local file equal remote file size if transfer was successful
            


    
    def cleanENV(self):
        operationlist=['']
        for op in operationlist:
            self.runcommand(op)



            

        



