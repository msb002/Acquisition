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
import threading
import LaserVis_layout
import glob
import datetime
import pandas as pd

from PyQt5 import QtCore, QtWidgets

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter, FuncFormatter

class MyDynamicMplCanvas(FigureCanvas):
    def __init__(self, mainwindow, parent = None, width =5, height = 4, dpi = 100):
        self.mainwindow = mainwindow #reference of main window so that those class funcitons can be called

        mpl.rcParams.update({'font.size': 12})
        #setup the figure
        self.fig, self.axes= plt.subplots(1,2,figsize = (width,height), dpi=dpi)
        self.axes[0].set_ylabel('Intensity (counts)')
        self.axes[0].set_xlabel('Gate Delay (ns)')
        self.axes[1].set_ylabel('Gate Delay of Peak (ns)')
        self.axes[1].set_xlabel('Time ')
        
        
        self.compute_initial_figure()
        FigureCanvas.__init__(self,self.fig)
        FigureCanvas.setSizePolicy(self,QtWidgets.QSizePolicy.Expanding,QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.setParent(parent)

    def compute_initial_figure(self):
        self.dataline1 = self.axes[0].plot([], [], 'r')
        self.dataline2 = self.axes[1].plot([], [], 'r')

    def update_data(self,intensities,gatedelaymax,gatedelaymax_time):
        #updates the figure with a new channel. 

        for ax in self.axes:
            ax.set_prop_cycle(None)
            for line in ax.lines:
                 ax.lines.remove(line)

        # self.axes[0].lines.remove(self.dataline1)
        # self.axes[1].lines.remove(self.dataline2)

        self.dataline1 = self.axes[0].plot(intensities)
        self.dataline2 = self.axes[1].plot(gatedelaymax_time,gatedelaymax)

        # leg = self.axes.legend_
        # if leg is not None:
        #     leg.remove()
        #     self.axes.legend()
        
        try:
            self.fig.tight_layout()
            self.fig.autofmt_xdate()
        except:
            print('could not run tight_layout, legend is probably too large')
        self.draw()
        
class Ui_MainWindow(LaserVis_layout.Ui_MainWindow):
    def __init__(self):
        self.gatedelaymax = []
        self.gatedelaymax_time = []

    def link_buttons(self):
        self.plotwidget = MyDynamicMplCanvas(self,self.centralwidget, width = 5, height = 4, dpi = 100)
        self.plotwidget.setGeometry(self.mplframe.geometry())
        self.plotwidget.setObjectName("widget")
        # self.pushButton_update.clicked.connect(self.plot_data)

    def open_saved_image(self, directory):
        # Access previously saved image
        if( os.path.exists(directory)):        
            files = glob.glob(directory +'/*.spe')
            if len(files) > 0: 
                last_image_acquired = max(files, key=os.path.getctime)
                # try:

                # time.sleep(5)
                while(True):
                    try:
                        intensities, timestamps, gatedelays = mhdpy.post.spe._lasertiming([last_image_acquired])
                    except IOError:
                        # print('File is not done writing yet, waiting')
                        time.sleep(1)
                    else:
                        break
                    
                    
                return intensities
                # except IOError:
                #     print ("Error: can not find file or read data")
                #     return None
        else:
            print(".spe file not found...")
            return None

    def plot_data(self,directory):
        intensities = self.open_saved_image(directory)
        if intensities is not None:
            self.gatedelaymax.append(intensities.idxmax())
            self.gatedelaymax_time.append(datetime.datetime.now())
            self.plotwidget.update_data(intensities,self.gatedelaymax, self.gatedelaymax_time)
            

class FolderMonitor(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.directory = "E:\\Data\\Raw Data\\2018-12-07\\Logfiles\\BeamTiming\\"
        self.files = glob.glob(self.directory +'/*.spe')
        self.runthread = True
    def run(self):
        while(self.runthread):
            
            filesnew = glob.glob(self.directory +'/*.spe')
            # print("new"+"\r\n" + str(filesnew) + "\r\n")
            # print("old" +"\r\n" + str(self.files) + "\r\n")
            if(filesnew != self.files):
                print("plotting new data point")
                self.files = filesnew
                ui.plot_data(self.directory)
            time.sleep(1)

app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.link_buttons()
MainWindow.show()

monitor = FolderMonitor()
monitor.start()


sys.exit(app.exec_())
