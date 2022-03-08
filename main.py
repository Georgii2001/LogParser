#!/usr/bin/env python
import re

HOST = r'^(?P<host>.*?)'
SPACE = r'\s'
IDENTITY = r'\S+'
USER = r'\S+'
TIME = r'(?P<time>\[.*?\])'
REQUEST = r'\"(?P<request>.*?)\"'
STATUS = r'(?P<status>\d{3})'
SIZE = r'(?P<size>\S+)'


regex = HOST+SPACE+IDENTITY+SPACE+USER+SPACE+TIME+SPACE+REQUEST+SPACE+STATUS+SPACE+SIZE+SPACE
numberOfElements=0
myList=[]

#--------------------------------------------------------------------------------------
def GroupByIp(myList):
   exists = False
   listIp = []
   for line in myList:
       exists=False
       for r in listIp:
           if r[0] == line[0]:
               exists=True
               break
       if exists==False:
           listIp.append([line[0],0,0,0])
   return listIp

def GroupByHttp(myList):
   exists = False
   listHttp = []
   for line in myList:
       exists=False
       for r in listHttp:
           if r[0] == line[3]:
               exists=True
               break
       if exists==False:
           listHttp.append([line[3],0,0,0])
   return listHttp

#-----------------------------------------------------------------------
def Count(list,position):
    for line in myList:
        for line2 in list:
            if line[position]==line2[0]:
                line2[1]=line2[1]+1
                break


def Percentage(list,position):
    Count(list,position)
    for line in list:
        line[2]=line[1]*100/numberOfElements

def BytesTransferred(list,position):
    for line in list:
        for line2 in myList:
            if line[0]==line2[position]:
                line[3]+=line2[4]


def Print(rows,myList,i):
    list = sorted(myList, key=lambda x: (x[i]), reverse=True)
    if rows != "":
        rows = int(rows)
        for line in list:
            print(f'{line[0]}: {line[i]}')
            rows -= 1
            if rows == 0:
                break
    else:
        for line in list:
            print(f'{line[0]}: {line[i]}')

#-----------------------------------------------------------------------
if __name__ == '__main__':
    filename = 'log'
    with open(filename, 'r') as logfile:
        for line in logfile:
            numberOfElements+=1
            match = re.search(regex, line)
            ip=match.group('host')
            time=match.group('time')
            request= match.group('request')
            http=match.group('status')
            if match.group('size') == '-':
                size = 0
            else:
                size = int(match.group('size'))
            myList.append([ip,time,request,http,size])

    listIp=GroupByIp(myList)
    listHttp=GroupByHttp(myList)

    while True:
       choise=input("Enter your choise(ip or http or 0- End of program): ")
       if choise=='0':
           break
       if choise=='ip':
           request=input("1- Request count; \n2- Request count percentage of all logged requests \n3- Total number of bytes transferred;\n")
           rows=input("Rows:")
           position=0
           if request=='1':
               Count(listIp,position)
               Print(rows,listIp,int(request))
           if request == '2':
               Percentage(listIp,position)
               Print(rows, listIp, int(request))
           if request == '3':
               BytesTransferred(listIp,position)
               Print(rows, listIp, int(request))
       if choise=='http':
           request = input("1- Request count; \n2- Request count percentage of all logged requests \n3- Total number of bytes transferred;\n")
           rows = input("Rows:")
           position=3
           if request == '1':
               Count(listHttp,position)
               Print(rows, listHttp, int(request))
           if request == '2':
               Percentage(listHttp,position)
               Print(rows, listHttp, int(request))
           if request == '3':
               BytesTransferred(listHttp,position)
               Print(rows, listHttp, int(request))
