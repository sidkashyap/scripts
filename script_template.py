import matplotlib.pyplot as plt
import numpy as np 
import sys

fig,axs = plt.subplots(nrows=1,ncols=1)

read_file = open(str(sys.argv[1]))
write_file = open(str(sys.argv[2]))
# If you need to open a file instead:
#f = open('your.file')

write = []
read = []
time_r = []
time_w = []
count = 0
flag = 0

for line in read_file:
    line.rstrip()
    if (count == 0):
        count = count + 1
        continue
    fields = line.strip().split(',')
    if (len(fields)<4):
        continue
    time_r.append(fields[3])
    read.append(fields[4])

count = 0
for line in write_file:
    line.rstrip()
    if (count == 0):
        count = count + 1 
        continue
    fields = line.strip().split(',')
    if (len(fields)<4):
        continue
    time_w.append(fields[3])
    write.append(fields[4])

write_S = [str(x) for x in write]
read_S = [str(x) for x in read]
time_r = [str(x) for x in time_r]
time_w = [str(x) for x in time_w]

axs.plot(time_w,write,  label='Write',ls='',marker='+')
axs.plot(time_r,read, label='Read',color='r',ls='',marker='o')

#axs.set_xticks(np.log2(nodes))
#axs.set_xticklabels(nodes_s)

#for x,y,z in zip(np.log2(nodes),write,write_S):
#    axs.text(x,y,z)
#for x,y,z in zip(np.log2(nodes),read,read_S):
#    axs.text(x,y,z)

#axs.set_xlim([0,8])
#axs.set_ylim([50,800])

plt.xlabel('Time')
plt.ylabel('Max BW, MiB/s')
plt.title('Graph')
plt.legend()
plt.show()
