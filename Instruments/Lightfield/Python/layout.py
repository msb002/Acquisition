# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'layout.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 266)
        MainWindow.setStatusTip("")
        MainWindow.setAccessibleName("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 15, 81, 16))
        self.label.setObjectName("label")
        self.lineEdit_exp1name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_exp1name.setEnabled(True)
        self.lineEdit_exp1name.setGeometry(QtCore.QRect(10, 35, 113, 22))
        self.lineEdit_exp1name.setText("")
        self.lineEdit_exp1name.setObjectName("lineEdit_exp1name")
        self.comboBox_settingname = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_settingname.setGeometry(QtCore.QRect(150, 30, 161, 22))
        self.comboBox_settingname.setObjectName("comboBox_settingname")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 10, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(150, 60, 71, 16))
        self.label_3.setObjectName("label_3")
        self.pushButton_sendexp1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_sendexp1.setGeometry(QtCore.QRect(330, 60, 141, 28))
        self.pushButton_sendexp1.setObjectName("pushButton_sendexp1")
        self.lineEdit_gatestart = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_gatestart.setGeometry(QtCore.QRect(10, 210, 71, 22))
        self.lineEdit_gatestart.setObjectName("lineEdit_gatestart")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(20, 190, 71, 16))
        self.label_5.setObjectName("label_5")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(-10, 170, 441, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.pushButton_start = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_start.setGeometry(QtCore.QRect(10, 120, 111, 28))
        self.pushButton_start.setObjectName("pushButton_start")
        self.lineEdit_exp2name = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_exp2name.setEnabled(True)
        self.lineEdit_exp2name.setGeometry(QtCore.QRect(10, 80, 113, 22))
        self.lineEdit_exp2name.setText("")
        self.lineEdit_exp2name.setObjectName("lineEdit_exp2name")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(30, 60, 81, 16))
        self.label_6.setObjectName("label_6")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(130, -3, 20, 181))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.pushButton_sendexp2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_sendexp2.setGeometry(QtCore.QRect(330, 90, 141, 28))
        self.pushButton_sendexp2.setObjectName("pushButton_sendexp2")
        self.pushButton_pullexp1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_pullexp1.setGeometry(QtCore.QRect(330, 120, 141, 28))
        self.pushButton_pullexp1.setObjectName("pushButton_pullexp1")
        self.lineEdit_settingname = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_settingname.setGeometry(QtCore.QRect(330, 30, 91, 22))
        self.lineEdit_settingname.setObjectName("lineEdit_settingname")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(330, 10, 141, 16))
        self.label_7.setObjectName("label_7")
        self.lineEdit_numframes = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_numframes.setGeometry(QtCore.QRect(170, 210, 71, 22))
        self.lineEdit_numframes.setObjectName("lineEdit_numframes")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(180, 190, 71, 16))
        self.label_8.setObjectName("label_8")
        self.lineEdit_gateend = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_gateend.setGeometry(QtCore.QRect(250, 210, 71, 22))
        self.lineEdit_gateend.setObjectName("lineEdit_gateend")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(260, 190, 71, 16))
        self.label_9.setObjectName("label_9")
        self.lineEdit_gatewidth = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_gatewidth.setGeometry(QtCore.QRect(90, 210, 71, 22))
        self.lineEdit_gatewidth.setObjectName("lineEdit_gatewidth")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(100, 190, 71, 16))
        self.label_10.setObjectName("label_10")
        self.pushButton_calcgate = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_calcgate.setGeometry(QtCore.QRect(360, 183, 91, 28))
        self.pushButton_calcgate.setObjectName("pushButton_calcgate")
        self.pushButton_updategate = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_updategate.setGeometry(QtCore.QRect(360, 213, 91, 28))
        self.pushButton_updategate.setObjectName("pushButton_updategate")
        self.pushButton_pullexp2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_pullexp2.setGeometry(QtCore.QRect(330, 150, 141, 28))
        self.pushButton_pullexp2.setObjectName("pushButton_pullexp2")
        self.pushButton_save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_save.setGeometry(QtCore.QRect(420, 30, 51, 28))
        self.pushButton_save.setObjectName("pushButton_save")
        self.settings_elements = QtWidgets.QTextBrowser(self.centralwidget)
        self.settings_elements.setGeometry(QtCore.QRect(150, 80, 161, 91))
        self.settings_elements.setObjectName("settings_elements")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionReload_ppr = QtWidgets.QAction(MainWindow)
        self.actionReload_ppr.setObjectName("actionReload_ppr")
        self.actionOpen_Eventlog = QtWidgets.QAction(MainWindow)
        self.actionOpen_Eventlog.setObjectName("actionOpen_Eventlog")
        self.actionToggle_Legend = QtWidgets.QAction(MainWindow)
        self.actionToggle_Legend.setObjectName("actionToggle_Legend")
        self.actionOpen_Cutting_Times = QtWidgets.QAction(MainWindow)
        self.actionOpen_Cutting_Times.setObjectName("actionOpen_Cutting_Times")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Post Processor"))
        self.label.setText(_translate("MainWindow", "Experiment 1"))
        self.label_2.setText(_translate("MainWindow", "Setting name"))
        self.label_3.setText(_translate("MainWindow", "Elements"))
        self.pushButton_sendexp1.setText(_translate("MainWindow", "Send to Experiment 1"))
        self.label_5.setText(_translate("MainWindow", "Gate Start"))
        self.pushButton_start.setText(_translate("MainWindow", "Start"))
        self.label_6.setText(_translate("MainWindow", "Experiment 2"))
        self.pushButton_sendexp2.setText(_translate("MainWindow", "Send to Experiment 2"))
        self.pushButton_pullexp1.setText(_translate("MainWindow", "Pull from Experiment 1"))
        self.label_7.setText(_translate("MainWindow", "Setting Name for saving"))
        self.label_8.setText(_translate("MainWindow", "# Frames"))
        self.label_9.setText(_translate("MainWindow", "Gate End"))
        self.label_10.setText(_translate("MainWindow", "Gate Width"))
        self.pushButton_calcgate.setText(_translate("MainWindow", "Calculate"))
        self.pushButton_updategate.setText(_translate("MainWindow", "Update Setting"))
        self.pushButton_pullexp2.setText(_translate("MainWindow", "Pull from Experiment 2"))
        self.pushButton_save.setText(_translate("MainWindow", "Save"))
        self.actionOpen.setText(_translate("MainWindow", "Open Logfile"))
        self.actionReload_ppr.setText(_translate("MainWindow", "Reload PPR"))
        self.actionOpen_Eventlog.setText(_translate("MainWindow", "Open Eventlog"))
        self.actionToggle_Legend.setText(_translate("MainWindow", "Toggle Legend"))
        self.actionOpen_Cutting_Times.setText(_translate("MainWindow", "Open Cutting Times"))

