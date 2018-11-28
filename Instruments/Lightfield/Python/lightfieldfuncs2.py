# Import the .NET class library
import clr
import sys
import os
import mhdpy
import time 
import json

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

    experiment.SetValue(CameraSettings.GatingMode,settings['GatingMode'])
    if settings['GatingMode'] == 1: #repetitive
        set_repetitive_gate(experiment, settings['GatingRepetitiveGate_Width'],settings['GatingRepetitiveGate_Delay'])
    elif settings['GatingMode'] == 2: #sequential
        set_sequential_gating(experiment, settings['GatingSequentialStartingGate_Width'], settings['GatingSequentialStartingGate_Delay'], settings['GatingSequentialEndingGate_Width'], settings['GatingSequentialEndingGate_Delay'])
def get_settings(experiment):
    settings = {}
    settings['Accumulations'] = experiment.GetValue(CameraSettings.ReadoutControlAccumulations)

    settings['GatingMode'] = experiment.GetValue(CameraSettings.GatingMode)
    settings['GatingRepetitiveGate_Delay'] = experiment.GetValue(CameraSettings.GatingRepetitiveGate).Delay
    settings['GatingRepetitiveGate_Width'] = experiment.GetValue(CameraSettings.GatingRepetitiveGate).Width
    settings['GatingSequentialEndingGate_Delay'] = experiment.GetValue(CameraSettings.GatingSequentialEndingGate).Delay
    settings['GatingSequentialStartingGate_Delay'] = experiment.GetValue(CameraSettings.GatingSequentialStartingGate).Delay
    settings['GatingSequentialEndingGate_Width'] = experiment.GetValue(CameraSettings.GatingSequentialEndingGate).Width
    settings['GatingSequentialStartingGate_Width'] = experiment.GetValue(CameraSettings.GatingSequentialStartingGate).Width

    settings['NumFrames'] = experiment.GetValue(ExperimentSettings.AcquisitionFramesToStore)
    return settings 

def read_settings(filepath):
    with open(filepath) as fp:
        settingsdict = json.load(fp)
    return settingsdict

def write_setting(filepath,setting, name):
    settings = read_settings(filepath)
    settings[name] = setting
    with open(filepath , 'w') as fp:
        json.dump(settings, fp)
    

def set_repetitive_gate(experiment, width, delay):
    # Check Gating Mode existence
    if (experiment.Exists(CameraSettings.GatingMode)):

        # Set repetitive gating mode
        experiment.SetValue(CameraSettings.GatingMode, GatingMode.Repetitive)  
        
        pulses = []

        # Add PI Pulse type with parameters to pulser list
        pulses.append(Pulse(width,delay))

        # Set repetitive gate
        experiment.SetValue(
            CameraSettings.GatingRepetitiveGate,
            pulses[0])
    else:
        print("System not capable of Gating Mode")
        
def set_sequential_gating(experiment, starting_width, starting_delay,
                   ending_width, ending_delay):
    # Check Gating Mode existence
    if (experiment.Exists(CameraSettings.GatingMode)):

        # Set sequential gating mode
        experiment.SetValue(CameraSettings.GatingMode, 
                            GatingMode.Sequential)   
        
        pulser = []

        # Add PI Pulse type with parameters to pulser list
        pulser.append(Pulse(starting_width, starting_delay))

        # Add PI Pulse type with parameters to pulser list
        pulser.append(Pulse(ending_width,ending_delay))      

        # Set sequential starting gate
        experiment.SetValue(
            CameraSettings.GatingSequentialStartingGate,
            pulser[0])

        # Set sequential ending gate
        experiment.SetValue(
            CameraSettings.GatingSequentialEndingGate,
            pulser[1])
    else:
        print("System not capable of Gating Mode")
        

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