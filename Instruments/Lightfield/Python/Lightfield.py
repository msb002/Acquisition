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
from PrincetonInstruments.LightField.Automation import Automation

from PrincetonInstruments.LightField.AddIns import Pulse 


from lightfieldfuncs2 import get_settings, set_settings, FilePathThread
            
curfolder = os.path.dirname(os.path.realpath(__file__))
filepath = os.path.join(curfolder,"settings.json")
with open(filepath) as fp:
    settingsdict = json.load(fp)

auto = Automation(True, List[String]())
experiment = auto.LightFieldApplication.Experiment
experiment.Load("TestCamera")
# fpthread = FilePathThread(experiment)
# fpthread.start()


# auto2 = Automation(True, List[String]())
# experiment2 = auto2.LightFieldApplication.Experiment
# experiment2.Load("TestCamera2")
# fpthread2 = FilePathThread(experiment2)
# fpthread2.start()