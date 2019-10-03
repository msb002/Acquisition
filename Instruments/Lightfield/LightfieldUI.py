# -*- coding: utf-8 -*-
"""
A post processing GUI function for parsing log files.

In general this Gui is used to call post processing functions from mhdpy.post. Some post processing functions want informaiton like a list of input files and times to parse those files by, and this GUI facilitates gathering that information. Use the vertical bars on the graph to select the desired parsing times, or select a time selection function to get a list of times (from the event log for instance).
"""

import mhdpy
import clr # Import the .NET class library
import sys
import os
import json
import time


from System.IO import * # Import System.IO for saving and opening files
from System import String # Import C compatible List and String
from System.Collections.Generic import List

sys.path.append(os.environ['LIGHTFIELD_ROOT'])# Add needed dll references
sys.path.append(os.environ['LIGHTFIELD_ROOT']+"\\AddInViews")
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')

import lightfieldfuncs as lf


from PyQt5 import QtCore, QtWidgets, QtGui

progname = os.path.basename(sys.argv[0]) #What is this?
progfolder = os.path.dirname(sys.argv[0])
progversion = "0.1"

experimentsfolder = 'C:\\Users\\bowenm\\Documents\\LightField\\Experiments'
import os 

import layout
class Ui_MainWindow(layout.Ui_MainWindow):
    """Main window of the post processor. Inherits from the MainWindow class within layout.py"""

    ###Initialization###
    def __init__(self):
        self.settingspath = os.path.join(progfolder, "settings.json")
        self.settings = {}     

    def setup(self):
        """links internal function to the various widgets in the main window"""
        self.pushButton_start.clicked.connect(self.start)

        regex = QtCore.QRegExp("[0-9_]+")
        validator = QtGui.QRegExpValidator(regex)
        self.lineEdit_gateend.setValidator(validator)
        self.lineEdit_gatestart.setValidator(validator)
        self.lineEdit_numframes.setValidator(validator)
        self.lineEdit_gatewidth.setValidator(validator)

        self.lineEdit_contacqdelay_exp1.setValidator(validator)
        self.lineEdit_contacqdelay_exp2.setValidator(validator)

        self.pushButton_pull.clicked.connect(self.pull_settings)
        self.pushButton_send.clicked.connect(self.send_settings)

        self.pushButton_startboth.clicked.connect(self.startboth)

        self.pushButton_calcgate.clicked.connect(self.calc_gateparams)
        self.pushButton_updategate.clicked.connect(self.update_gateparams)
        self.pushButton_save.clicked.connect(self.save_settings)
        self.pushButton_load.clicked.connect(self.load_button)
        self.pushButton_newsetting.clicked.connect(self.newsetting)

        #TODO: make this a lambda function passing the experiment
        self.radioButton_contacq_exp1.released.connect(self.continuousacq_exp1)
        self.radioButton_contacq_exp2.released.connect(self.continuousacq_exp2)

        self.comboBox_settingname.currentIndexChanged.connect(self.settingname_updated)
        self.comboBox_expname.currentIndexChanged.connect(self.experimentname_updated)

        #Populate experiment names

        onlyfiles = [f for f in os.listdir(experimentsfolder) if os.path.isfile(os.path.join(experimentsfolder, f))]
        experimentlist = [os.path.splitext(f)[0] for f in onlyfiles]
        experimentlist.append("")
        self.comboBox_exp1.insertItems(0,experimentlist)
        self.comboBox_exp2.insertItems(0,experimentlist)
        if(len(experimentlist)>1):
            self.comboBox_exp2.setCurrentIndex(1)

        #load in settings

        self.load_settings()

    def load_settings(self):
        if os.path.exists(self.settingspath):
            with open(self.settingspath,'r') as fileread:
                try:
                    self.settings = json.load(fileread)
                except json.decoder.JSONDecodeError:
                    print('Could not read settings')
                    self.settings = {}       
        else:
            print('setting file doesnt exist') 
            self.settings = {}

    def load_button(self):
        self.load_settings()
        self.experimentname_updated()

    def start(self):
        exp1name = self.comboBox_exp1.currentText()
        exp2name = self.comboBox_exp2.currentText()
        
        self.logfilearr = [] #Whether LF instances are set to 'logging' mode

        #TODO: get rid of this list by using dict.items()
        self.exparr = [] 
        self.expdict = {}
        if(exp1name != ""): 
            self.logfilearr.append(bool(self.checkBox_logfileexp1.checkState()))
            self.exp1 = lf.LFexp(exp1name)
            self.exparr.append(self.exp1)
            self.expdict[exp1name] = self.exp1
        if(exp2name != ""):
            self.logfilearr.append(bool(self.checkBox_logfileexp2.checkState()))
            self.exp2 = lf.LFexp(exp2name)
            self.exparr.append(self.exp2)
            self.expdict[exp2name] = self.exp2
        #Start monitor threads which monitor filename changes and write to the eventlog
        lfthread = lf.LFMonitorThread(self)
        lfthread.start()
        
        for experimentname in self.expdict.keys():
            experiment = self.expdict[experimentname]
            settings = lf.get_settings(experiment.exp)
            if not experimentname in self.settings:
                self.settings[experimentname] = {}
            self.settings[experimentname]['default'] = settings
            
        self.comboBox_expname.insertItems(0,self.expdict.keys())
        # self.experimentname_updated()

    def experimentname_updated(self):
        #When changing experiment name, update the settings selector
        experimentname = self.comboBox_expname.currentText()
        self.expsettings = self.settings[experimentname]
        
        #Insert new settings into setting selector and update the list of settings
        self.comboBox_settingname.blockSignals(True)
        self.comboBox_settingname.clear()
        self.comboBox_settingname.insertItems(0,self.expsettings.keys())
        self.settingname_updated()
        self.comboBox_settingname.blockSignals(False)


    def settingname_updated(self):
        experimentname = self.comboBox_expname.currentText()
        settingname = self.comboBox_settingname.currentText()
        setting = self.settings[experimentname][settingname]
        
        settingliststr = ""

        for key in setting:
            settingliststr = settingliststr + key + ":\r\n" + str(setting[key]) + "\r\n"

        self.settings_elements.setText(settingliststr)
        self.lineEdit_settingname.setText(settingname)

        #Update gate calculator
        self.lineEdit_gatestart.setText(str(int(setting['GatingSequentialStartingGate_Delay'])))
        #self.lineEdit_gateend.setText(setting['GatingSequentialEndingGate_Delay'])
        self.lineEdit_gatewidth.setText(str(int(setting['GatingSequentialStartingGate_Width'])))
        self.lineEdit_numframes.setText(str(int(setting['NumFrames'])))
        self.calc_gateparams()

    def send_settings(self,expstr):
        #Send settings to experiment
        experimentname = self.comboBox_expname.currentText()
        experiment = self.expdict[experimentname]
        settingname = self.comboBox_settingname.currentText()
        setting = self.settings[experimentname][settingname]
        lf.set_settings(experiment.exp,setting)

    def pull_settings(self):
        #Get settings from experiment
        experimentname = self.comboBox_expname.currentText()
        experiment = self.expdict[experimentname]
        setting = lf.get_settings(experiment.exp)
        settingname = self.comboBox_settingname.currentText()
        self.settings[experimentname][settingname] = setting
        self.settingname_updated()


    def calc_gateparams(self):
        start = int(self.lineEdit_gatestart.text())
        num = int(self.lineEdit_numframes.text())
        width = int(self.lineEdit_gatewidth.text())

        end = start + (num-1)*width

        self.lineEdit_gateend.setText(str(end))

    def update_gateparams(self):
        #Puts calculated gate params into internal setting, does not send to experiment. 
        experimentname = self.comboBox_expname.currentText()
        settingname = self.comboBox_settingname.currentText()
        self.settings[experimentname][settingname]['GatingSequentialStartingGate_Delay'] =  int(self.lineEdit_gatestart.text())
        self.settings[experimentname][settingname]['GatingSequentialStartingGate_Width'] =  int(self.lineEdit_gatewidth.text())
        self.settings[experimentname][settingname]['GatingSequentialEndingGate_Delay'] =  int(self.lineEdit_gateend.text())
        self.settings[experimentname][settingname]['GatingSequentialEndingGate_Width'] =  int(self.lineEdit_gatewidth.text())
        self.settings[experimentname][settingname]['NumFrames'] =  int(self.lineEdit_numframes.text())
        self.settingname_updated()

    def newsetting(self):
        #Copy the current setting to a new item in the dict
        cursettingname = self.comboBox_settingname.currentText()
        newsettingname = self.lineEdit_settingname.text()
        experimentname = self.comboBox_expname.currentText()
        self.settings[experimentname][newsettingname] = self.settings[experimentname][cursettingname]
        num = self.comboBox_settingname.count()
        self.comboBox_settingname.insertItem(num,newsettingname)
        self.comboBox_settingname.setCurrentIndex(num)

    def save_settings(self):
        with open(self.settingspath , 'w') as fp:
            json.dump(self.settings, fp)
        self.load_settings()
        self.experimentname_updated()

    def continuousacq_exp1(self):
        #Start a logging thread which constantly restarts acquisition. 
        if(self.radioButton_contacq_exp1.isChecked()):
            self.lt_exp1 = lf.LoggingThread(self, 'exp1')
            self.lt_exp1.start()
        else:
            self.lt_exp1.logging = False
            self.exp1.exp.Stop()

    def continuousacq_exp2(self):
        #Start a logging thread which constantly restarts acquisition. 
        if(self.radioButton_contacq_exp2.isChecked()):
            self.lt_exp2 = lf.LoggingThread(self, 'exp2')
            self.lt_exp2.start()
        else:
            self.lt_exp2.logging = False
            self.exp2.exp.Stop()


    def startboth(self):
        self.radioButton_contacq_exp1.click()
        self.radioButton_contacq_exp2.click()
        # self.continuousacq_exp1()
        # self.continuousacq_exp2()
    
app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.setup()
MainWindow.show()


sys.exit(app.exec_())
