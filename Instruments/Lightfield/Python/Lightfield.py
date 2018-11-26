import mhdpy
import time

fileinfo = mhdpy.daq.get_fileinfo()

filepath = mhdpy.daq.gen_filepath('Lightfield', '.spe')

while(True):
    fileinfonew = mhdpy.daq.get_fileinfo()
    if(fileinfonew != fileinfo):
        fileinfo = fileinfonew
        filepath = mhdpy.daq.gen_filepath('Lightfield', '.spe')
        print(filepath)
    time.sleep(0.1)

