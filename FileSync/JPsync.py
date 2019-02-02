import os
import datetime
import numpy as np
import pandas as pd

JPpath = 'H:\\Data\\JP8000'
rawdatapath = 'H:\\Data\\Raw Data'

from shutil import copyfile

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

