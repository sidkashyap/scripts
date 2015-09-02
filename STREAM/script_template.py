from __future__ import division
import matplotlib.pyplot as plt
import numpy as np 
import sys
import re



threads_pattern = re.compile(r'Number of Threads counted =')
copy_pattern = re.compile(r'Copy:')
add_pattern= re.compile(r'Add:')
scale_pattern=re.compile(r'Scale:')
triad_pattern=re.compile(r'Triad:')

i=0
numThreads = []
copyBW = []
addBW=[]
scaleBW=[]
triadBW=[]

chartTitle=""


write_bandwidth_mean = []

colors = ['b','g','r','c','m','y','k']


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
        line_check = re.search(threads_pattern, line)
        if(line_check):
            
            thread_split = line.split()
            threads = thread_split[5]
            numThreads.append(threads)
            continue

        line_check = re.search(copy_pattern, line)
        if(line_check):
            copy_split = line.split()
            temp = copy_split[1]
            copyBW.append(temp)
            continue

        line_check = re.search(add_pattern, line)
        if(line_check):
            add_split = line.split()
            temp = add_split[1]
            addBW.append(temp)
            continue

        line_check = re.search(scale_pattern, line)
        if(line_check):
            scale_split = line.split()
            temp = scale_split[1]
            scaleBW.append(temp)
            continue

        line_check = re.search(triad_pattern, line)
        if(line_check):
            triad_split = line.split()
            temp = triad_split[1]
            triadBW.append(temp)
            continue



            
def plotFile():


    numThreads_i = [int(x) for x in numThreads]
    triad_S = [str(x) for x in triadBW]
    scale_S =  [str(x) for x in scaleBW]
    add_S = [str(x) for x in addBW]
    copy_S = [str(x) for x in copyBW]

    axs.plot(np.log2(numThreads_i), triadBW, label='triad',marker='o', linestyle='--')
    axs.plot(np.log2(numThreads_i), copyBW, marker='+', linestyle='-', color='r', label='copy')
    axs.plot(np.log2(numThreads_i), addBW, marker='*', linestyle='-', color='m', label='add')
    axs.plot(np.log2(numThreads_i), scaleBW, marker='_', linestyle='-', color='y', label='scale')
	

    
       
    axs.set_xticks(np.log2(numThreads_i))
    axs.set_xticklabels(numThreads)

    for x,y,z in zip(np.log2(numThreads_i),triadBW,triad_S):
        axs.text(x,y,z)

    for x,y,z in zip(np.log2(numThreads_i),copyBW,copy_S):
        axs.text(x,y,z)
    for x,y,z in zip(np.log2(numThreads_i),addBW,add_S):
       axs.text(x,y,z)
    for x,y,z in zip(np.log2(numThreads_i),scaleBW,scale_S):
    	axs.text(x,y,z)


### MAIN #####


width=0.1
counter=1
Title = ""
for stream_file in sys.argv[1:]:

    if("Title" in stream_file):
        Title=stream_file
        continue
    
    IOR_file = open(str(stream_file))
    read_file = IOR_file.readlines()
    line_count=len(stream_file)
    processFile(read_file)
    counter=counter+1


plotFile()

# add some text for labels, title and axes ticks
axs.set_ylabel('Max Bandwidth, MiB/s')
axs.set_xlabel('Number of Threads')

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

#plt.title(Title,fontsize=16,fami
API = ['triad','copy','add','scale']
axs.legend(API, loc='best', bbox_to_anchor=(1, 0.5),
          fancybox=True, shadow=True)

plt.show()










