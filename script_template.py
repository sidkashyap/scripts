from __future__ import division
import matplotlib.pyplot as plt
import numpy as np 
import sys
import re



grep_pattern = re.compile(r'Summary of all tests:')

i=0
write = []
read = []
API=[]


write=[]
read=[]
flag=0

transferSize=0
fileSize=0
filePP=0
tasksPerNode=0
readMax=0.0
readMin=0.0
readMean=0.0
writeMax=0.0
writeMin=0.0
writeMean=0.0
NumberOfNodes=0
blockSize=0.0


write_nodes = []
read_nodes = []


read_bandwidth_max = []
write_bandwidth_max = []

read_bandwidth_min = []
write_bandwidth_min = []

read_bandwidth_mean = []


chartTitle=""


write_bandwidth_mean = []

colors = ['b','g','r','c','m','y','k']

#IOR_Summary = Enum('Operation','Max','Min','Mean','StdDev','Mean','TestNum','Tasks','tPN','reps','fPP','reord','reordoff','reordrand','seed', 'segcnt', 'blksiz', 'xsize', 'aggsize', 'API', 'RefNum')
class IOR_Summary:
    Operation=0
    Max=1
    Min=2
    Mean=3
    StdDev=4
    Mean=5
    TestNum=6
    Tasks=7
    tPN=8
    reps=9
    fPP=10
    reord=11
    reordoff=12
    reordrand=13
    seed=14
    segcnt=15
    blksiz=16
    xsize=17
    aggsize=18
    API=19
    RefNum=20
    

fig,axs = plt.subplots()
rects=[]


def autolabel(rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            axs.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                    ha='center', va='bottom')


def processFile(file_contents):
    line_count=len(file_contents)
    flag=0
    for i in range(line_count):
        line = read_file[i]
        line.rstrip()
        line_check = re.search(grep_pattern, line)
        if(line_check):
            i=i+2
            write = read_file[i].split()
            i=i+1
            read = read_file[i].split()
            transferSize=float(read[IOR_Summary.xsize])/(1024*1024)
            fileSize=int(read[IOR_Summary.aggsize])

            fileSize= fileSize / (1024*1024*1024)
            blockSize= int(read[IOR_Summary.blksiz]) / (1024*1024*1024)
            filePP=int(read[IOR_Summary.fPP])
            tasksPerNode=int(read[IOR_Summary.tPN])
            
            if(flag==0):
                rAPI=read[IOR_Summary.API]
                rAPI=rAPI+" read "

                wAPI= write[IOR_Summary.API]
                wAPI = wAPI+" write "


                API.append(wAPI)
                API.append(rAPI)


                global chartTitle
                chartTitle ="FilePerProcess = %d\nFile Size = %dgB\nTransfer Size = %dmB" % (filePP, fileSize, transferSize)
                flag=1




           
            if("inf" in read[IOR_Summary.Max] or "nan" in read[IOR_Summary.Max] ):
                print "here "+read[IOR_Summary.Max]
                read[IOR_Summary.Max]= 0
            if("inf" in write[IOR_Summary.Max] or "nan" in write[IOR_Summary.Max]):
                print "here "+write[IOR_Summary.Max]
                write[IOR_Summary.Max]= 0

            readMax=float(read[IOR_Summary.Max])
            writeMax=float(write[IOR_Summary.Max])
            NumberOfNodes=int(read[IOR_Summary.Tasks])

            if(NumberOfNodes ==1 or NumberOfNodes ==2 ):
                print "here123"

            

            write_nodes.append(NumberOfNodes)
            read_nodes.append(NumberOfNodes)

            write_bandwidth_max.append(writeMax)
           
            read_bandwidth_max.append(readMax)

def plotFile(counter):

    one=[]
    two=[]
    basewidth=0.1
    init = counter -1;


    
    width1 = counter/10 + (counter-1)/10
    width2= width1+basewidth

    color1 = colors[counter+init]
    color2 = colors[counter+init+1]
    
    one = np.log2(read_nodes)+width1
    rects1 = axs.bar(one, write_bandwidth_max, basewidth,color=color1)
    rects.append(rects1)

    two = np.log2(read_nodes)+width2
    rects2 = axs.bar(two, read_bandwidth_max, basewidth,color=color2)
    rects.append(rects2)




### MAIN #####


width=0.1
counter=1
Title = ""
for IOR_file_i in sys.argv[1:]:

    if("Title" in IOR_file_i):
        Title=IOR_file_i
        continue
        

    write_bandwidth_max=[]
    read_bandwidth_max=[] 
    read_nodes=[]

    
    IOR_file = open(str(IOR_file_i))
    read_file = IOR_file.readlines()
    line_count=len(read_file)
    processFile(read_file)
    plotFile(counter)
    counter=counter+1


# add some text for labels, title and axes ticks
axs.set_ylabel('Max Bandwidth, MiB/s')
axs.set_xlabel('Number of Nodes')

font = {'family' : 'monospace',
        'color'  : 'black',
        'weight' : 'normal',
        'size'   : 12,
        }

Title = Title.replace("Title:", "")

# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

# place a text box in upper left in axes coords
axs.text(0.05, 0.95, chartTitle, transform=axs.transAxes, fontsize=14,
        verticalalignment='top', bbox=props, fontdict=font)



plt.text(0.5, 1.08, Title, horizontalalignment='center', family='monospace',fontsize=20,  transform = axs.transAxes)

#plt.title(Title,fontsize=16,family='monospace',y=0.9)
axs.set_xticks(np.log2(read_nodes)+0.1)
axs.set_xticklabels(read_nodes)
#axs.legend(API, loc='best', bbox_to_anchor=(1, 0.5),fancybox=True, shadow=True)

axs.legend(API, loc='best', bbox_to_anchor=(1, 0.5))
for i in rects:
    autolabel(i)

plt.show()










