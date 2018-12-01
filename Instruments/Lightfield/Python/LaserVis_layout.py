# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LaserVis_layout.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(476, 398)
        MainWindow.setStatusTip("")
        MainWindow.setAccessibleName("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.mplframe = QtWidgets.QWidget(self.centralwidget)
        self.mplframe.setGeometry(QtCore.QRect(10, 10, 451, 341))
        self.mplframe.setObjectName("mplframe")
        self.pushButton_update = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_update.setGeometry(QtCore.QRect(30, 360, 93, 28))
        self.pushButton_update.setObjectName("pushButton_update")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Post Processor"))
        self.pushButton_update.setText(_translate("MainWindow", "Update"))

