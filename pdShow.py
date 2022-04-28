#!/usr/bin/env python

##########################################################################
#	CopyRight	(C)	THORNBIRD,2030	All Rights Reserved!
#
#	Module:		Excel File to jpg
#
#	File:		pdShow.py
#
#	Author:		thornbird
#
#	Date:		2022-04-15
#
#	E-mail:		wwwthornbird@163.com
#
###########################################################################

###########################################################################
#
#	History:
#	Name		Data		Ver		Act
#--------------------------------------------------------------------------
#	thornbird	2022-04-15	v1.0		create
#
###########################################################################

import sys,os,re,string,time,datetime
import pandas as pd

SW_VERSION='0.1'

SortData=1
ZeroFilter=1
fileName=''

SaveFileName='' #'ScanData.txt'

DefaultScanFileType=('.xlsx','.csv')
DefaultCols=['xxx','Total']

ScanPath=''

# log var
debugLog = 0
debugLogLevel=(0,1,2,3)	# 0:no log; 1:op logic; 2:op; 3:verbose

class FileScan:
        Tags = 'FileScan'
        __dirname=''
        __filename=''
        __fd=''

        __df=''

        def __init__(self,dirname,filename,fd):
            self.__dirname=dirname
            self.__filename=filename
            self.__fd=fd
            self.__fileLines=0


        def Check(self,cols):
            if debugLog >= debugLogLevel[-1]:
                print('Check: ',self.__filename,cols)
            
            if ZeroFilter:
                if debugLog >= debugLogLevel[2]:
                    print('Drop Zero Data!')
                self.__df=fd[cols].dropna()
            else:
                self.__df=fd[cols]

 
            if SortData:
                if debugLog >= debugLogLevel[2]:
                    print('Sort Data!')
                self.__df=self.__df.sort_values(by=DefaultCols[-1])
            
            if debugLog >= debugLogLevel[2]:
                print("Data: \n",self.__df)

        def __SaveFile(self,filename,data):
            if data:
                if filename:
                    fname = filename.split('.')[0] 
                    f= fname+'.xlsx'
                    data.to_excel(f)

                    f= fname+'.jpg' 
                    data.plot(x=DefaultCols[0],grid=True,rot=45,figsize=(15,15)).get_figure().savefig(f)  

                if debugLog >= debugLogLevel[2]:
                    print( 'Save file: '+f)
            else:
                if debugLog >= debugLogLevel[2]:
                    print( '(WARN) Save File len is 0!')

        def SaveToFile(self,fd):
            if debugLog >= debugLogLevel[-1]:
                print( 'SaveToFile:')

            self.__SaveFile(self.__filename,__self.__df)

        def Dump(self):
            if debugLog >= debugLogLevel[-1]:
                print( 'Dump:')

        def getFileName(self):
            return os.path.join(self.__dirname,self.__filename)

#Global Data
class ScanFileType:
        global DefaultScanFileType

        __Scans={}
        __ScanFiles=DefaultScanFileType

        __Col=''

        __fileType=0	#0:.xlsx; 1:.csv

        def SetScanTags(self,Class,ScanTags):
            if debugLog >= debugLogLevel[-1]:
                print( '(INFO) Set ScanDirs : ',ScanTags)
            self.__Scans[Class]=ScanTags

        def SetScanFiles(self,ScanFiles):
            if debugLog >= debugLogLevel[-1]:
                print( '(INFO) Set ScanFiles : ',ScanFiles)
            self.__ScanFiles=ScanFiles
        
        def GetScanFiles(self):
            if debugLog >= debugLogLevel[-1]:
                print( '(INFO) Get ScanFiles')
            return self.__ScanFiles

        def GetScans(self):
            if debugLog >= debugLogLevel[-1]:
                print( '(INFO) Get Scans ')
            return self.__Scans

        def SetCol(self,col):
            if debugLog >= debugLogLevel[-1]:
                print( '(INFO) Set Col: ',col)
            self.__Col = col  
            return self.__Scans
	
        def GetCol(self):
            if debugLog >= debugLogLevel[-1]:
                print( '(INFO) Get Col: ')
            return self.__Col

        def Dump(self):
            print( 'Scans: ',self.__Scans)

#global var
ScanFiles = ScanFileType()
Datas=[]

def FileCheck(dirname,filename,fd):
    if debugLog >= debugLogLevel[-1]:
        print( 'Scan Log:  '+filename)

    fScan = FileScan(dirname,filename,fd)
    
    fScan.Check(DefaultCols)

    Datas.append(fScan)

def ScanFile(dirname,file):
    if debugLog >= debugLogLevel[-1]:
        print( 'Scan File:\n '+dirname+file)

    if debugLog >= debugLogLevel[2]:
        print( "(INFO) Match File Type: ",ScanFiles.GetScanFiles())
    
    Types = ScanFiles.GetScanFiles()

    #for file in files:

    for i in range(0,len(Types)):
        if debugLog >= debugLogLevel[-1]:
            print( "File Match Format: "+Types[i])
      
          
        fileType = re.compile(Types[i])

        if debugLog >= debugLogLevel[-1]:
            print( file)
		
        m = re.search(fileType,file)
        if m:
            path,name = os.path.split(dirname)

            if debugLog >= debugLogLevel[-1]:
                print( 'Find Dir: '+dirname)
		
            if debugLog >= debugLogLevel[1]:
                print( 'Find Match File: '+file)

            try:
                #fd = open(os.path.join(dirname,file),'rb')
			
                if debugLog >= debugLogLevel[-1]:
                       print( 'INFO: open file :'+os.path.join(dirname,file))

                fd = pd.read_exce(os.path.join(dirname,file),'rb')
                FileCheck(dirname,file,fd)

                #fd.close()

            except IOError:
                print( "open file ERROR: Can't open"+os.path.join(dirname,file))

def SaveData(filename,datas):
    if debugLog >= debugLogLevel[-1]:
        print( 'SaveData Begin: ',filename)

    try:
        fo = open(filename,"wt")

        fo.write('Scan Total Files: '+str(len(datas))+'\n')
        
        fo.write('Files:\n')
        for i in range(0,len(datas)):
            fo.write(datas[i].getFileName()+'\n')
        fo.write('\n\n')

        for i in range(0,len(datas)):
            datas[i].SaveToFile(fo)

    except IOError:
        print( "Error: Can't open or write!!!")
    else:
        fo.close()

        print( '\nSaveFile: ',filename)

def ScanDir(Dir):
    CamDirs=[]
    print( 'Scan DIR: '+Dir+'\n')

    #os.path.walk(Dir,ScanFile,())
    #print(os.listdir(Dir))
    with os.scandir(Dir) as it:
        for entry in it:
            if not entry.name.startswith('.') and entry.is_file():
                ScanFile(Dir,entry.name)
    
    if SaveFileName:
        SaveData(SaveFileName,Datas)


def ParseArgv():
	if len(sys.argv) > appParaNum+1:
		HelpInfo()
		sys.exit()
	else:
		for i in range(1,len(sys.argv)):
			if sys.argv[i] == '-h':
				Usage()
				sys.exit()
			elif sys.argv[i] == '-d':
				if sys.argv[i+1]:
					debug = int(sys.argv[i+1])
					if type(debug) == int:
						global debugLog
						debugLog = debug						
						print( 'Log level is: '+str(debugLog))
					else:
						print( 'cmd para ERROR: '+sys.argv[i+1]+' is not int num!!!')
				else:
					CameraOpenKPIHelp()
					sys.exit()
			elif sys.argv[i] == '-o':
				if sys.argv[i+1]:
					global fileName
					fileName = sys.argv[i+1]
					print( 'OutFileName is '+fileName)
				else:
					Usage()
					sys.exit()
			elif sys.argv[i] == '-p':
				if sys.argv[i+1]:
					global ScanPath
					ScanPath = sys.argv[i+1]
					print( 'Scan dir path is '+ScanPath)
				else:
					Usage()
					sys.exit()
			elif sys.argv[i] == '-s':
					global SortData
					SortData = 1
					print( 'Sort is ',SortData)
			elif sys.argv[i] == '-z':
					global ZeroFilter
					ZeroFilter = 1
					print( 'ZeroFilter is ',ZeroFilter)


def Usage():
	print( 'Command Format :')
	print( '		CameraLogScan [-d 1/2/3] [-o output excel file] [-p path]  [-s] [-z Filt zero data]| [-h]')

appParaNum = 6

if __name__ == '__main__':
        print( 'Version: '+SW_VERSION)

        ParseArgv()

        if not ScanPath.strip():
                spath = os.getcwd()
        else:
                spath = ScanPath

        ScanDir(spath)
