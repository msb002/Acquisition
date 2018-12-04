# Import the .NET class library
import clr
import sys
import os
import mhdpy
import time

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

import win32com.client  # Python ActiveX Client
import threading

def set_settings(experiment,settings):
    experiment.SetValue(CameraSettings.ReadoutControlAccumulations, settings['Accumulations'])

def get_settings(experiment):
    settings = {}
    settings['Accumulations'] = experiment.GetValue(CameraSettings.ReadoutControlAccumulations)
    return settings 

class FilePathThread(threading.Thread):
    def __init__(self,experiment, name = "Lightfield", logfile = False):
        threading.Thread.__init__(self)
        self.experiment = experiment
        self.runthread = True

    def run(self):
        self.LabVIEW = win32com.client.Dispatch("Labview.Application") # when start is called a new thread is created and the COM object must be created in that thread
        self.fileinfo = ""
        while(self.runthread):
            self.fileinfonew = mhdpy.daq.get_fileinfo(self.LabVIEW )
            if(self.fileinfonew != self.fileinfo):
                self.fileinfo = self.fileinfonew
                self.filepath = mhdpy.daq.gen_filepath(self.LabVIEW ,'Lightfield', '.spe')
                folder = os.path.split(self.filepath)[0]
                filename = os.path.split(self.filepath)[1]
                self.experiment.SetValue(ExperimentSettings.FileNameGenerationDirectory,folder)
                self.experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName,filename)
            time.sleep(0.1)
    
    def exit(self):
        self.runthread = False