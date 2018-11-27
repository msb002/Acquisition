import mhdpy
import clr # Import the .NET class library
import sys
import os
import json


from System.IO import * # Import System.IO for saving and opening files
from System import String # Import C compatible List and String
from System.Collections.Generic import List

sys.path.append(os.environ['LIGHTFIELD_ROOT'])# Add needed dll references
sys.path.append(os.environ['LIGHTFIELD_ROOT']+"\\AddInViews")
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')

from lightfieldfuncs import LFexp, FilePathThread
            

tc1 = LFexp("TestCamera")
tc2 = LFexp("TestCamera2")

fpthread = FilePathThread([tc1,tc2])
fpthread.start()

