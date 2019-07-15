import clr
import sys
import os
import mhdpy
import time
import json

#repopath = os.path.split(os.path.split(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])[0])[0]

from System.IO import * # Import System.IO for saving and opening files
from System import String # Import C compatible List and String
from System.Collections.Generic import List

# Add needed dll references
sys.path.append(os.environ['LIGHTFIELD_ROOT'])
sys.path.append(os.environ['LIGHTFIELD_ROOT']+"\\AddInViews")
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')

# PI imports
from PrincetonInstruments.LightField.AddIns import CameraSettings
from PrincetonInstruments.LightField.AddIns import GatingMode
from PrincetonInstruments.LightField.AddIns import Pulse 
from PrincetonInstruments.LightField.AddIns import DeviceType   
from PrincetonInstruments.LightField.AddIns import ExperimentSettings

from PrincetonInstruments.LightField.Automation import Automation
import win32com.client  # Python ActiveX Client
import threading
import glob


class LightfieldApplication():
    
    def __init__(self):         
        self.auto = Automation(True, List[String]())
        self.experiment = self.auto.LightFieldApplication.Experiment

    def get_experiment(self):
        return self.experiment
    
    def close(self):
        self.auto.Dispose()


def add_available_devices():
    # Add first available device and return
    for device in experiment.AvailableDevices:
        print("\n\tAdding Device...")
        experiment.Add(device)
        return device
    
def save_file(filename):    
    # Set the base file name
    experiment.SetValue(
        ExperimentSettings.FileNameGenerationBaseFileName,
        Path.GetFileName(filename))
    
    # Option to Increment, set to false will not increment
    experiment.SetValue(
        ExperimentSettings.FileNameGenerationAttachIncrement,
        False)

    # Option to add date
    experiment.SetValue(
        ExperimentSettings.FileNameGenerationAttachDate,
        True)

    # Option to add time
    experiment.SetValue(
        ExperimentSettings.FileNameGenerationAttachTime,
        True)

		
		
		
def get_paths(exp):
    LabVIEW = win32com.client.Dispatch("Labview.Application")
    filepath = mhdpy.daq.gen_filepath(LabVIEW , exp.Name,'', DAQmx = False, Logfile= True)
    folder = os.path.split(filepath)[0]
    filename = os.path.split(filepath)[1]
    return [folder,filename]
	
	

app1 = LightfieldApplication()
exp1 = app1.get_experiment()
exp1.Load('TransmCam')
#exp1.SetValue(ExperimentSettings.FileNameGenerationDirectory,get_paths(exp1)[0])
#exp1.SetValue(ExperimentSettings.FileNameGenerationBaseFileName,get_paths(exp1)[1])
#exp1.SetValue(ExperimentSettings.FileNameGenerationAttachDate,True)
#exp1.SetValue(ExperimentSettings.FileNameGenerationAttachTime,True)

app2 = LightfieldApplication()
exp2 = app2.get_experiment()
exp2.Load('ReflCam')
#exp2.SetValue(ExperimentSettings.FileNameGenerationDirectory,get_paths(exp2)[0])
#exp2.SetValue(ExperimentSettings.FileNameGenerationBaseFileName,get_paths(exp2)[1])
#exp2.SetValue(ExperimentSettings.FileNameGenerationAttachDate,True)
#exp2.SetValue(ExperimentSettings.FileNameGenerationAttachTime,True)


i=0
while i<10:
    exp1.Acquire()
    exp2.Acquire()
    time.sleep(1)
    i+=1
	
	
app1.close()
app2.close()