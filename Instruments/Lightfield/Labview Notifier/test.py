# -*- coding: utf-8 -*-
"""
Various functions for conversions of time objects
"""
import datetime
import os

libname = 'win32com.client'
try:
    lib = __import__(libname)
except:
    print('failed loading win32com...')
else:
    globals()[libname] = lib

import win32com.client  # Python ActiveX Client



# repopath = os.path.split(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])[0]

repopath = os.path.dirname(os.path.abspath(__file__))

vipath = os.path.join(repopath, 'testnotifier.vi')

LabVIEW = win32com.client.Dispatch("Labview.Application")

VI = LabVIEW.getvireference(vipath)  # Path to LabVIEW VI
VI._FlagAsMethod("Run")

VI.setcontrolvalue('a', 1)
VI.setcontrolvalue('b', 2)
VI.Run()  # Run the VI
c = VI.getcontrolvalue('c')

print(c)