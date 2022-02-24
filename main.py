#!/usr/bin/env python
import sys
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
listIp=[]
listHttp=[]

def OrderDescByBytes():
    list = sorted(listIp, key = lambda x: (x[4]), reverse= True)
    for line in list:
        print(line)

def GroupByIp():
    for line in listIp:
        print(line)

def GroupByHttp():
    for line in listHttp:
        print(line)

def RequestCount(request):
    sum=0
    for line in listIp:
        if line[2]==request:
            sum=sum+1
    return sum

def TotalNumberBytes():
    sum = 0
    for line in listIp:
        sum+=line[4]
    return sum

def RowsPrinted(rowsNumber):
    for line in listIp:
        print(line)
        rowsNumber-=1
        if rowsNumber==0:
            break

def RequestPercentage():
   ok = 0
   listReq = []
   for line in listIp:
       for r in listReq:
           if r == line[2]:
               ok=1
               break
       if ok==0:
           listReq.append(line[2])
           print(f' {line[2]}  -  {RequestCount(line[2])/numberOfElements*100} %')






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
            listIp.append([ip,time,request,http,size])
            listHttp.append([http,ip, time, request, size])

    while 1:
        print(
            "1- Group by Ip; \n2- Group by Http; \n3- Request count; \n4- Request count percentage of all logged requests; "
            "\n5- Total number of bytes transferred;\n6-Print the results in descending order by bytes;\n7-Limit the number of rows printed;"
            "\n0- End of program   ")
        choise=input("Enter your choise: ")
        if choise=='1':
            GroupByIp()
        elif choise=='2':
            GroupByHttp()
        elif choise=='3':
            req=input("Request:")
            try:
                print(RequestCount(req))
            except:
                print("0")
        elif choise=='4':
            RequestPercentage()
        elif choise=='5':
            print(TotalNumberBytes())
        elif choise=='6':
            OrderDescByBytes()
        elif choise=='7':
            rowsNumber=input("The number of rows printed: ")
            RowsPrinted(int(rowsNumber))
        elif choise=='0':
            print("End of program.")
            break







