import json
import paramiko
import subprocess
import os
import platform
#import ntpath


class Pkg:
    def __init__(self,packagepath):
        #curdir=os.getcwd()
        #pkgpath=os.path.join(curdir,packagepath)
        self.packagepath=packagepath
        self.packagesize=os.stat(packagepath).st_size
        self.packagename=os.path.basename(packagepath)
        #self.packagesize=os.stat(pkgpath).st_size
    
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
        #cwd=os.getcwd()
        pkg=os.path.split(self.packagepath)
        '''os.path.join(cwd,'pkg')
        pkg=os.path.join(pkgpath,self.packagename)
        filestats=os.stat(pkg)
        self.packagesize=filestats/(1024*1024)
        print(self.packagesize)'''
        pkgenvironment=self.checkpkgENV()
        os.chdir(pkg[0])
        subprocess.run('tar -zcvf '+self.packagename.strip()+'.tar.gz '+self.packagepath,capture_output=True)
        '''if pkgenvironment['os'].lower() == 'linux':
            subprocess.run('tar -zcvf '+self.packagename+'.tar.gz '+pkg,capture_output=True)
        elif pkgenvironment['os'].lower() == 'windows':
            subprocess.run('compact /c '+pkg+' /I /Q')'''
            #run windows archiving
        newpath=os.path.join(pkg[0],self.packagename.strip()+'.tar.gz')
        return newpath,self.packagename+'.tar.gz'.strip()
    
    def getprops(self): 
        pkgprops={}
        pkgprops['path']=self.packagepath
        pkgprops['name']=self.packagename
        pkgprops['size']=self.packagesize
        #get package name
        return pkgprops

    def preppkg(self):
        #run dos2unix on scripts before deploying 
        curdir=os.getcwd()
        manifestpath=os.path.join(curdir,'pkg/'+self.packagename+'/manifest.json')
        if os.path.isfile(manifestpath):
            with open(manifestpath,'r') as manifestfile:
                manifest=json.load(manifestfile)
        else:
            scriptname=input('Enter name of first script to run\n')
            manifest={'init':[scriptname]}
            with open(manifestpath,'w') as manifestfile:
                json.dump(manifest,manifestfile)
        initscript=os.path.join(curdir,'script/loaderscript.sh')
        with open(initscript,'w+') as start:
            start.write('sh '+manifest['init']+';sh '+manifest['verification'])
        if self.checkpkgENV()['os'].lower()=='windows':
            winexecpath=os.path.join(curdir,'dependency/dos2unix/dos2unix.exe')
            ret=subprocess.run(winexecpath+' '+initscript)
            if ret.returncode == 0:
                return True
        return False

    def unbox(self):
        #unzip package on remote server 
        pass

