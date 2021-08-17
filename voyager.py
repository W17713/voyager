#!/usr/bin/env python3
import execution_seq
from Remoteserver import Remoteserver
import sys

def addIPs():
    print('Welcome to voyager.\nChoose an option to add IPs\n')
    print('1.Add IP range\n')
    print('2.Add random IPs from IP list\n')
    stepone=input()
    if stepone==str(1):
        print('Add IP range as follows FirstNodeIP-LastNodeID e.g 10.249.249.10-20\n')
        steponeInput=input()
        steponeOut=execution_seq.addIPrange(steponeInput)
        if steponeOut=='successful':
            print('IP range was added succesfully\n')
    elif stepone==str(2):
        print('Add each IP address on a newline. Press enter to proceed to add next IP\nInput \"done\" when you are done adding IPlist\n')
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
    print('Please enter the username for servers\n')
    username=input().strip()
    print('Please enter the password for servers\n')
    password=input().strip()
    return username,password

def remoteTests(username,password):
    iplist=execution_seq.getIPs()
    for i in iplist:
        print('Running tests on remote servers now\n')
        rms=Remoteserver(i.strip(),22,username.strip(),password.strip())
        pingstatus,pingout=rms.ping()
        print(pingout)
        if pingstatus:
            print('ping test completed successfully\n')
            sshstatus,sshout=rms.runcommand()
            print(sshout)
            if sshstatus:
                print('ssh test completed successfully\n')
                sftpstatus,sftpout=rms.sftpcheck()
                print(sftpout)
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

def shipPackage():
    print('All tests passed. Do you want to deploy package? (Y/N)')
    answer=input().lower()
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
            rms.deployPackage()
    elif answer in answers[1]: #if answer is any form on no
        print('All tests completed successfully. Enter a yes to proceed or q to quit.\n')
        response=input()
        if response in answers[0]:
            Remoteserver.deployPackage()
        elif response=='q':
            sys.exit()
    else:
        print('Please enter a Yes/No.\n')
        lastresponse=input()
        if lastresponse in answers[0]:
            Remoteserver.deployPackage()
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
        shipPackage()
    else:
        print('Tests failed')

