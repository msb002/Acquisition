import os
import datetime
# import numpy as np
# import pandas as pd
from shutil import copyfile




JPpath = 'H:\\Data\\JP8000'
rawdatapath = 'H:\\Data\\Raw Data'

fns = [fn for fn in os.listdir(JPpath) if os.path.isfile(os.path.join(JPpath,fn))]

for fn in fns:
    fp = os.path.join(JPpath,fn)
    mtime = os.path.getmtime(fp)
    dt = datetime.datetime.fromtimestamp(mtime)
    folderstr = dt.strftime("%Y-%m-%d")
    outfolder = os.path.join(rawdatapath,folderstr + "\\Logfiles\\JP\\")
    if not os.path.exists(outfolder):
        os.makedirs(outfolder)
    outpath = os.path.join(outfolder,fn)
    if os.path.exists(outpath):
        print(outpath + ' Already exists...skipping')
    else:
        print('copying ' + outpath)
        copyfile(fp,outpath)

input("Press enter to continue...")

"""
To build into an excecutable use pyinstaler.

If encountering a recursion error follow instructions here:
https://stackoverflow.com/questions/38977929/pyinstaller-creating-exe-runtimeerror-maximum-recursion-depth-exceeded-while-ca

to create the .spec file
pyinstaller JPsync.py -c --onefile 

Then close out and add the lines to spec file

import sys
sys.setrecursionlimit(5000)

then run 

pyinstaller JPsync.spec   
"""
