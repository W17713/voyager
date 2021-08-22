#!/usr/bin/env python3
import execution_seq
from Remoteserver import Remoteserver
import sys
import os
import json

def addIPs():
    print('Welcome to voyager.\nChoose an option to add IPs\n')
    print('1.Add range of IPs\n')
    print('2.Add non range hosts from list\n')
    print('3.Load existing host group\n')
    stepone=input()
    if stepone==str(1):
        steponeInput=input('Add IP range as follows FirstNodeIP-LastNodeID e.g 10.249.249.10-20\n')
        steponeOut=execution_seq.addIPrange(steponeInput)
        if steponeOut=='successful':
            print('IP range was added succesfully\n')
    elif stepone==str(2):
        print('Add each hostname or IP address on a newline. Press enter to proceed to add next IP\nInput \"done\" when you are done adding hosts\n')
        iplist=[]
        steptwoInput=input()
        while steptwoInput != 'done':
            if steptwoInput !='\n':
                iplist.append(steptwoInput)
                steptwoInput=input()
        steptwoOut=execution_seq.addIPrandom(iplist)
        if steptwoOut=='successful':
            print('IPs were added succesfully\n')
    elif stepone==str(3):
        list=os.listdir(os.path.join(os.getcwd(),'asset/hosts'))
        #print(list)
        if len(list) != 0:
            print('Choose host group from list\n')
            for i,j in enumerate(list):
                print(str(i+1)+'. '+j)
            hostgrpid=int(input())
            hostgrpdict= execution_seq.loadHosts(list[hostgrpid-1])
        else:
            nohoststep=input('There are no existing host groups\n')
        return True,hostgrpdict
    return False,execution_seq.getIPs()

def getCredentials(hosts):
    hostdict={}
    passtype=input('Choose 1 to use the same username and password for all hosts\nChoose 2 to enter different usernames and passwords for each\n')
    if passtype == str(1):
        username=input('Please enter the username for servers\n').strip()
        password=input('Please enter the password for servers\n').strip()
        #append same cred for all hosts in hostlist 
        for host in hosts:
            hostdict[host]={'username':username,'password':password} 
        hostgrpname=input('Enter name of host group \n')
    elif int(passtype) == 2:
        #add credentials to host dictionary
        for host in hosts:
            username=input('Enter username for '+host+'\n').strip()
            password=input('Enter password for '+host+'\n').strip()
            hostdict[host]={'username':username,'password':password}  
        hostgrpname=input('Enter name of host group \n')
    else:
        ('Choose between 1 and 2\n')
    hostsfile=open(os.path.join(os.getcwd(),'asset/'+hostgrpname+'.json'),'w')
    json.dump(hostdict,hostsfile)
    hostsfile.close()
    return hostdict

def remoteTests(hosts):
    for id,host in hosts.items():
        print('Running tests on remote servers now\n')
        rms=Remoteserver(id.strip(),22,host['username'].strip(),host['password'].strip())
        pingstatus,pingout=rms.ping()
        #print(pingout)
        if pingstatus:
            print('ping test completed successfully\n')
            sshstatus,sshout=rms.runcommand()
            print('Remote System Info: '+sshout[0])
            if sshstatus:
                print('ssh test completed successfully\n')
                sftpstatus,sftpout=rms.sftpcheck()
                #print(sftpout)
                if sftpstatus:
                    print('sftp test completed successfully\n')
                    if pingstatus and sshstatus and sftpstatus == True:
                        return True,'success'
                else:
                    error='could not transfer files to host'
            else:
                error='Could not ssh into host'
        else:
            error='Could not ping host'
    print(error)
    return False,error

def choosePackage():
    packages=os.listdir(os.path.join(os.getcwd(),'pkg'))
    options=[]
    print('All tests passed. Choose package to deploy\n')
    for i,p in enumerate(packages):
        options.append(i+1)
        print(str(i+1)+'. '+p)
    #print(options)
    inp=0
    option=int(input())
    if option in options or inp in options:
        chosenpkg=packages[option-1]
    else:
        inp=input('Choose package again. Your option is not in the list\n')
    return chosenpkg
    
def shipPackage(pkg,hosts):
    answer=input('Do you want to deploy package? (Y/N)').lower()
    answerOptions=['Yes','No']
    answers=[[],[]] #list os lists to store variations or yes and no
    for h,i in enumerate(answerOptions):
        answers[h].append(i)
        answers[h].append(i[0])
        answers[h].append(i[0].lower())
        answers[h].append(i.lower())
        answers[h].append(i.upper())
    if answer in answers[0]: #if answer is any form of yes [upper,lower,Y,Capitalized]
        #iplist=execution_seq.getIPs()
        for id,host in hosts.items():
            print('Deploying package to remote servers now\n')
            rms=Remoteserver(id.strip(),22,host['username'].strip(),host['password'].strip())
            rms.deployPackage(pkg)
    elif answer in answers[1]: #if answer is any form on no
        response=input('Enter a yes to deploy package or q to quit.\n')
        if response in answers[0]:
            Remoteserver.deployPackage(pkg)
        elif response=='q':
            sys.exit()
    else:
        lastresponse=input('Please enter a Yes/No.\n')
        if lastresponse in answers[0]:
            Remoteserver.deployPackage(pkg)
        elif lastresponse in answers[1]:
            print('Not deploying package')
        else:
            sys.exit()



if __name__=="__main__":
    status,IPs=addIPs()
    if len(IPs) !=0:
        if status == False: #if host group does not exist, get credentials 
            hosts=getCredentials(IPs)
        else:
            hosts=IPs #if host group exists, pass directly to remote tests
        testresults,msg=remoteTests(hosts)
    if testresults:
        pkg=choosePackage()
        shipPackage(pkg,hosts)
    else:
        print('Tests failed')

