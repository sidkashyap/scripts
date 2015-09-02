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
            threads = (int)thread_split[5]
            numThreads.append(threads)
            continue

        line_check = re.search(copy_pattern, line)
        if(line_check):
            copy_split = line.split()
            temp = (float)copy_split[1]
            copyBW.append(temp)
            continue

        line_check = re.search(add_pattern, line)
        if(line_check):
            add_split = line.split()
            temp = (float)add_split[1]
            addBW.append(temp)
            continue

        line_check = re.search(scale_pattern, line)
        if(line_check):
            scale_split = line.split()
            temp = (float)scale_split[1]
            scaleBW.append(temp)
            continue

        line_check = re.search(triad_pattern, line)
        if(line_check):
            triad_split = line.split()
            temp = (float)triad_split[1]
            triadBW.append(temp)
            continue



            
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
for stream_file in sys.argv[1:]:

    if("Title" in stream_file):
        Title=stream_file
        continue
    
    IOR_file = open(str(stream_file))
    read_file = stream_file.readlines()
    line_count=len(stream_file)
    processFile(read_file)
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
axs.legend(API, loc='best', bbox_to_anchor=(1, 0.5),
          fancybox=True, shadow=True)



for i in rects:
    autolabel(i)

plt.show()










