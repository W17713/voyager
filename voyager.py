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
        print('1.Add IP range as follows FirstNodeIP-LastNodeID e.g 10.249.249.10-20\n')
        steponeInput=input()
        steponeOut=execution_seq.addIPrange(steponeInput)
        if steponeOut=='successful':
            print('IP range was added succesfully\n')
    elif stepone==str(2):
        print('1.Add all IPs in IPlist.txt file in assets/IPlistfile.txt\n')
        steptwoInput=input()
        steptwoOut=execution_seq.addIPrange(steptwoInput)
        if steponeOut=='successful':
            print('IP range was added succesfully\n')
    return execution_seq.getIPs()
def getCredentials():
    print('Please enter the username for servers\n')
    username=input()
    print('Please enter the password for servers\n')
    password=input()
    return username,password

def remoteTests(username,password):
    iplist=execution_seq.getIPs()
    for i in iplist:
        print('Running tests on remote servers now\n')
        rms=Remoteserver(i,22,username,password)
        pingstatus,pingout=rms.ping()
        sshstatus,sshout=rms.connect()
        sftpstatus,sftpout=rms.checkftp()
        if pingstatus:
            print('ping test completed successfully\n')
        if sshstatus:
            print('ssh test completed successfully\n')
        if sftpstatus:
            print('sftp test completed successfully\n')
    if pingstatus and sshstatus and sftpstatus == True:
        return True
    return False

def shipPackage():
    print('All tests passed. Do you want to deploy package? (Y/N)')
    answer=lower(input())
    answerOptions=['Yes','No']
    answers=[]
    yesanswers=[]
    noanswers=[]
    answers.append(yesanswers)
    answers.append(noanswers)
    for h,i in enumerate(answerOptions):
        answers[h].append(i)
        answers[h].append(i[0])
        answers[h].append(i.lower())
        answers[h].append(i.upper())
    if answer in answers[0]: #if answer is any form of yes [upper,lower,Y,Capitalized]
        Remoteserver.deployPackage()
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
            Remoteserver.deployPackage()
        else:
            sys.exit()



if __name__=="__main__":
    IPs=addIPs()
    if len(IPs) !=0:
        username,password=getCredentials()
        testresults=remoteTests(username,password)
    if testresults:
        shipPackage()
    else:
        print('Tests failed')

