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

import layout
class Ui_MainWindow(layout.Ui_MainWindow):
    """Main window of the post processor. Inherits from the MainWindow class within layout.py"""

    ###Initialization###
    def __init__(self):

        self.settingspath = os.path.join(progfolder, "settings.json")
        
        with open(self.settingspath,'r') as fileread:
            try:
                self.settings = json.load(fileread)
            except json.decoder.JSONDecodeError:
                print('Could not read settings')
                self.settings = {}
        
    def save(self):
        with open(self.settingspath , 'w') as fp:
            json.dump(self.settings, fp)
    
    def setup(self):
        """links internal function to the various widgets in the main window"""
        self.pushButton_start.clicked.connect(self.start)

        self.comboBox_settingname.insertItems(0,self.settings.keys())
        self.settingname_updated()
        self.comboBox_settingname.currentIndexChanged.connect(self.settingname_updated)

        self.lineEdit_exp1name.setText("TestCamera")
        self.lineEdit_exp2name.setText("TestCamera2")

        regex = QtCore.QRegExp("[0-9_]+")
        validator = QtGui.QRegExpValidator(regex)
        self.lineEdit_gateend.setValidator(validator)
        self.lineEdit_gatestart.setValidator(validator)
        self.lineEdit_numframes.setValidator(validator)
        self.lineEdit_gatewidth.setValidator(validator)

        self.pushButton_pullexp1.clicked.connect(lambda : self.pull_settings(self.exp1.exp))
        self.pushButton_pullexp2.clicked.connect(lambda : self.pull_settings(self.exp2.exp))
        self.pushButton_sendexp1.clicked.connect(lambda : self.send_settings(self.exp1.exp))
        self.pushButton_sendexp2.clicked.connect(lambda : self.send_settings(self.exp2.exp))

        self.pushButton_calcgate.clicked.connect(self.calc_gateparams)
        self.pushButton_updategate.clicked.connect(self.update_gateparams)
        self.pushButton_save.clicked.connect(self.save)

    def start(self):
        exp1name = self.lineEdit_exp1name.text()
        exp2name = self.lineEdit_exp2name.text()
        exparr = []

        if(exp1name != ""):
            self.exp1 = lf.LFexp(exp1name)
            exparr.append(self.exp1)
        if(exp2name != ""):
            self.exp2 = lf.LFexp(exp2name)
            exparr.append(self.exp2)

        fpthread = lf.FilePathThread(exparr)
        fpthread.start()

    def settingname_updated(self):
        settingname = self.comboBox_settingname.currentText()
        setting = self.settings[settingname]
        # settinglist = [item for item in setting]
        
        settingliststr = ""

        for key in setting:
            settingliststr = settingliststr + key + ":\r\n" + str(setting[key]) + "\r\n"

        self.settings_elements.setText(settingliststr)
        self.lineEdit_settingname.setText(settingname)

        self.lineEdit_gatestart.setText(str(int(setting['GatingSequentialStartingGate_Delay'])))
        #self.lineEdit_gateend.setText(setting['GatingSequentialEndingGate_Delay'])
        self.lineEdit_gatewidth.setText(str(int(setting['GatingSequentialStartingGate_Width'])))
        self.lineEdit_numframes.setText(str(int(setting['NumFrames'])))
        self.calc_gateparams()

    def pull_settings(self,experiment):
        setting = lf.get_settings(experiment)
        settingname = self.comboBox_settingname.currentText()
        self.settings[settingname] = setting
        self.settingname_updated()

    def calc_gateparams(self):
        start = int(self.lineEdit_gatestart.text())
        num = int(self.lineEdit_numframes.text())
        width = int(self.lineEdit_gatewidth.text())

        end = start + num*width

        self.lineEdit_gateend.setText(str(end))

    def update_gateparams(self):
        settingname = self.comboBox_settingname.currentText()
        self.settings[settingname]['GatingSequentialStartingGate_Delay'] =  int(self.lineEdit_gatestart.text())
        self.settings[settingname]['GatingSequentialStartingGate_Width'] =  int(self.lineEdit_gatewidth.text())
        self.settings[settingname]['GatingSequentialEndingGate_Delay'] =  int(self.lineEdit_gateend.text())
        self.settings[settingname]['GatingSequentialEndingGate_Width'] =  int(self.lineEdit_gatewidth.text())
        self.settings[settingname]['NumFrames'] =  int(self.lineEdit_numframes.text())
        self.settingname_updated()

    def send_settings(self,experiment):
        settingname = self.comboBox_settingname.currentText()
        setting = self.settings[settingname]
        lf.set_settings(experiment,setting)

app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.setup()
MainWindow.show()


sys.exit(app.exec_())
