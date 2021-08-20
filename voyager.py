#!/usr/bin/env python3
import execution_seq
from Remoteserver import Remoteserver
import sys
import os

def addIPs():
    print('Welcome to voyager.\nChoose an option to add IPs\n')
    print('1.Add range of IPs\n')
    print('2.Add non range hosts from list\n')
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
    return execution_seq.getIPs()

def getCredentials():
    username=input('Please enter the username for servers\n').strip()
    password=input('Please enter the password for servers\n').strip()
    return username,password

def remoteTests(username,password):
    iplist=execution_seq.getIPs()
    for i in iplist:
        print('Running tests on remote servers now\n')
        rms=Remoteserver(i.strip(),22,username.strip(),password.strip())
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

def shipPackage(pkg):
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
        iplist=execution_seq.getIPs()
        for i in iplist:
            print('Deploying package to remote servers now\n')
            rms=Remoteserver(i.strip(),22,username.strip(),password.strip())
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
    IPs=addIPs()
    if len(IPs) !=0:
        username,password=getCredentials()
        testresults,msg=remoteTests(username,password)
    if testresults:
        pkg=choosePackage()
        shipPackage(pkg)
    else:
        print('Tests failed')

