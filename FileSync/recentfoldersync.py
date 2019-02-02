
import dirsync
import os
import datetime
import numpy as np
import pandas as pd

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

maxsize = 180 #mb
print('syncing all recent directories up to size ' + str(maxsize) + 'Mb')
maxsize = maxsize*1e6



f1 = 'C:\\Users\\aspit\\Documents\\synctest\\Folder 1\\'
f2 = 'C:\\Users\\aspit\\Documents\\synctest\\Folder 2\\'

folders = [ name for name in os.listdir(f1) if os.path.isdir(os.path.join(f1, name)) ]
dates = []
sizes = []
for i, folder in enumerate(folders):
    try:
        dates.append( datetime.datetime.strptime(folder,'%Y-%m-%d'))
    except ValueError:
        print('folder: \" ' + folder + ' \"  does not match data format')
        del folders[i]
    else:
        sizes.append(get_size( os.path.join(f1,folder)))

sizes = pd.Series(sizes, index = dates)
folders = pd.Series(folders, index = dates)

sizes = sizes.sort_index(ascending=False)
folders = folders.sort_index(ascending=False)

cumsize = np.cumsum(sizes)


#should replace at some point with a for loop over the recieving folder so that folders not in raw data anymore for some reason can be removed 
synced = []
unsynced = []
for date in cumsize.index:
    if cumsize[date] < maxsize:
        src = os.path.join(f1,folders[date]) 
        dst = os.path.join(f2,folders[date])
        print('syncing ' + folders[date])
        dirsync.sync(src,dst,'sync', create = True)
        synced.append(folders[date])
    else:
        unsynced.append(folders[date])

print('synced directories ' + str(synced))
print('unsynced directories ' + str(unsynced))
    
import shutil

for folder in unsynced:
    path = os.path.join(f2,folder)
    if os.path.exists(path):
        print('removing: ' + path)
        shutil.rmtree(path)
