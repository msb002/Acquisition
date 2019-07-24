# Import the .NET class library
import clr
import sys
import os
import mhdpy
import time
import json

repopath = os.path.split(os.path.split(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])[0])[0]

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


from PyQt5 import QtCore, QtWidgets

def set_settings(experiment,settings):
    experiment.SetValue(CameraSettings.ReadoutControlAccumulations, settings['Accumulations'])

    experiment.SetValue(CameraSettings.GatingMode,settings['GatingMode'])
    if settings['GatingMode'] == 1: #repetitive
        set_repetitive_gate(experiment, settings['GatingRepetitiveGate_Width'],settings['GatingRepetitiveGate_Delay'])
    elif settings['GatingMode'] == 2: #sequential
        set_sequential_gating(experiment, settings['GatingSequentialStartingGate_Width'], settings['GatingSequentialStartingGate_Delay'], settings['GatingSequentialEndingGate_Width'], settings['GatingSequentialEndingGate_Delay'])

    experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore,settings['NumFrames'])
    experiment.SetValue(ExperimentSettings.OnlineProcessingFrameCombinationFramesCombined,settings['ExposuresPerFrame'])

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
    settings['ExposuresPerFrame'] = experiment.GetValue(ExperimentSettings.OnlineProcessingFrameCombinationFramesCombined)
    
    # settings['CenterWavelength'] = experiment.GetValue(SpectrometerSettings.GratingCenterWavelength)    
    # settings['Grating'] = experiment.GetValue(SpectrometerSettings.Grating)    
    return settings 
   

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
        
def set_sequential_gating(experiment, starting_width, starting_delay, ending_width, ending_delay):
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
        
#???? 
# def set_simpoequential_gating_num(experiment, width, starting_delay,numframes):
#     experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore,numframes)
#     ending_delay = starting_delay + width*numframes
#     set_sequential_gating(experiment, width, starting_delay, width, ending_delay)

class LFexp():
    def __init__(self, expname):
        self.auto = Automation(True, List[String]())
        self.exp = self.auto.LightFieldApplication.Experiment
        self.exp.Load(expname)
        self.name = expname

    def set_setting(self,setting):
        set_settings(self.exp, setting)


class LFMonitorThread(threading.Thread):
    def __init__(self,explist, logfilearr):
        threading.Thread.__init__(self)
        self.explist= explist 
        self.runthread = True
        self.logfilearr = logfilearr
        self.runningdict = {}
        for exp in explist:
            self.runningdict[exp] = exp.exp.IsRunning

    def run(self):
        self.LabVIEW = win32com.client.Dispatch("Labview.Application") # when start is called a new thread is created and the COM object must be created in that thread
        self.fileinfo = ""
        for i, exp in enumerate(self.explist):
            logfile = self.logfilearr[i]
            filepath = mhdpy.daq.gen_filepath(self.LabVIEW , exp.name,'', DAQmx = False, Logfile= logfile)
            folder = os.path.split(filepath)[0]
            filename = os.path.split(filepath)[1]
            exp.exp.SetValue(ExperimentSettings.FileNameGenerationDirectory,folder)
            exp.exp.SetValue(ExperimentSettings.FileNameGenerationBaseFileName,filename)

        datafolder = mhdpy.daq.get_rawdatafolder(self.LabVIEW)
        if not os.path.exists(datafolder):
            os.makedirs(datafolder)
        el_path = os.path.join(datafolder,"Eventlog_Lightfield.json")
        with open(el_path, 'a+') as fp:
            fp.write("")
        self.eventlogwriter = mhdpy.eventlog.Eventlog(el_path)

        while(self.runthread):
            #Check for file info changes and send to experiments
            self.fileinfonew = mhdpy.daq.get_fileinfo(self.LabVIEW )
            if(self.fileinfonew != self.fileinfo):
                self.fileinfo = self.fileinfonew
                for i, exp in enumerate(self.explist):
                    logfile = self.logfilearr[i]
                    if not logfile:
                        if exp.exp.IsRunning:
                            print('cannot change test case while experiment is running and not in logging mode...stopping experiment')
                            """After some research I will have to switch this to a QtThread in order to send messages to the main window. So just stopping the experiment for now."""
                            exp.exp.Stop()
                            #The experiment takes a bit of time to stop so this while loop makes sure it is stopped before attempting to change the file name.
                            time.sleep(1)
                            while exp.exp.IsRunning:
                                print('Experiment not stopped yet...')
                                time.sleep(1)
                                
                        filepath = mhdpy.daq.gen_filepath(self.LabVIEW , exp.name,'', DAQmx = False, Logfile= logfile)
                        folder = os.path.split(filepath)[0]
                        filename = os.path.split(filepath)[1]
                        exp.exp.SetValue(ExperimentSettings.FileNameGenerationDirectory,folder)
                        exp.exp.SetValue(ExperimentSettings.FileNameGenerationBaseFileName,filename)

            #check if the experiments have changed their running state and write to the eventlog
            for exp in self.explist:
                if(exp.exp.IsRunning != self.runningdict[exp]):
                    self.runningdict[exp] = exp.exp.IsRunning
                    self.eventlogwriter.SavingVIsChange("LFpython_" + exp.exp.Name,exp.exp.IsRunning)

            time.sleep(0.1)
    
    def exit(self):
        self.runthread = False

class LoggingThread(threading.Thread):
    def __init__(self,experiment):
        threading.Thread.__init__(self)
        self.experiment = experiment
        self.logging = False

    def run(self):
        self.logging = True
        while(self.logging):
            self.experiment.Acquire()
            while(self.experiment.IsRunning):
                time.sleep(0.1)


    

# exp1 = LFexp('TestCamera')

# fp = 'C:\\Labview Test Data\\2018-11-30\\Logfiles\\TestCamera2\\'
# open_saved_image(fp)
# LabVIEW = win32com.client.Dispatch("Labview.Application")
# print(repopath)
# datafolder = mhdpy.daq.get_rawdatafolder(repopath,LabVIEW)