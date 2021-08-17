import paramiko
import subprocess
import os
import platform


class Pkg:
    def __init__(self,packagename):
        curdir=os.getcwd()
        pkgpath=os.path.join(curdir,packagename)
        pkg=os.listdir(pkgpath)
        self.packagename=pkg[0]
        fp=os.path.join(pkgpath,self.packagename)
        self.packagesize=os.stat(fp).st_size
    
    def checkpkgENV(self):
        ENV={}
        plt=platform.platform()
        os=platform.system()
        ENV['plt']=plt
        ENV['os']=os
        try:
            pyversion=subprocess.run('python --version',capture_output=True)
            ENV['pyversion']=pyversion.stdout.decode('utf-8').strip()
        except CalledProcessError as cpe:
            ENV['pyversion']='n/a'
        return ENV

    def box(self):
        #zip package
        cwd=os.getcwd()
        pkg=os.path.join(cwd,'pkg/'+self.packagename)
        filestats=os.stat(pkg)
        self.packagesize=filestats/(1024*1024)
        
        pkgenvironment=self.checkpkgENV()
        if pkgenvironment['os'].lower() == 'linux':
            subprocess.run('tar -zcvf '+self.packagename+'.tar.gz '+pkg,capture_output=True)
        elif pkgenvironment['os'].lower() == 'windows':
            subprocess.run('compact /c '+pkg+' /I /Q')
            #run windows archiving
    
    def getprops(self): 
        pkgprops={}
        pkgprops['name']=self.packagename
        pkgprops['size']=self.packagesize
        #get package name
        return pkgprops

    def preppkg(self):
        #run dos2unix on scripts before deploying 
        curdir=os.getcwd()
        winexecpath=os.path.join(curdir,'dependency/dos2unix/dos2unix.exe')
        pkgpath=os.path.join(curdir,'script/loaderscript.sh')
        if self.checkpkgENV()['os'].lower()=='windows':
            ret=subprocess.run(winexecpath+' '+pkgpath)
            if ret.returncode == 0:
                return True
        return False

    def unbox(self):
        #unzip package on remote server 
        pass

