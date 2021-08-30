# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import threading
import psutil
import os
import sys
import Cam
import wx
from PIL import ImageGrab
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui


class MyWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.retranslateUi

        self.Check_Timer = QtCore.QTimer(self)
        self.Check_Timer.setInterval(500)
        self.Check_Timer.timeout.connect(self.Hardware_Timer)

        self.Display_Timer = QtCore.QTimer(self)
        self.Display_Timer.setInterval(100)
        self.Display_Timer.timeout.connect(self.Display_Time)
        self.Display_Timer.start()

    def setupUi(self, Dialog):
        Dialog.setStyleSheet("color:black;" "background-color:#FFFFFF")
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.TimerOn = QPushButton(Dialog)
        self.TimerOn.setGeometry(QtCore.QRect(60, 240, 75, 23))
        self.TimerOn.setObjectName("TimerOn")
        self.TimerOn.setStyleSheet("color: green;"
                      "border-style: solid;"
                      "border-width: 4px;"
                      "border-color: #000000;"
                      "border-radius: 3px")
        self.TimerOff = QPushButton(Dialog)
        self.TimerOff.setGeometry(QtCore.QRect(140, 240, 75, 23))
        self.TimerOff.setObjectName("TimerOff")
        self.TimerOff.setStyleSheet("color: red;"
                      "border-style: solid;"
                      "border-width: 4px;"
                      "border-color: #000000;"
                      "border-radius: 3px")
        self.Capture = QPushButton(Dialog)
        self.Capture.setGeometry(QtCore.QRect(250, 240, 75, 23))
        self.Capture.setObjectName("Capture")

        self.Label_CPU = QLabel(Dialog)
        self.Label_CPU.setGeometry(QtCore.QRect(40, 80, 51, 21))
        self.Label_CPU.setObjectName("Label_CPU")
        self.progressBar_CPU = QProgressBar(Dialog)
        self.progressBar_CPU.setGeometry(QtCore.QRect(100, 80, 191, 23))
        self.progressBar_CPU.setProperty("value", 0)
        self.progressBar_CPU.setObjectName("progressBar_CPU")

        self.Label_RAM = QLabel(Dialog)
        self.Label_RAM.setObjectName("Label_RAM")
        self.Label_RAM.setGeometry(QtCore.QRect(40, 110, 51, 21))
        self.progressBar_RAM = QProgressBar(Dialog)
        self.progressBar_RAM.setGeometry(QtCore.QRect(100, 110, 191, 23))
        self.progressBar_RAM.setProperty("value", 0)
        self.progressBar_RAM.setObjectName("progressBar_RAM")

        self.retranslateUi(Dialog)
        self.TimerOn.clicked.connect(self.Timer_Start)
        self.TimerOff.clicked.connect(self.Timer_Stop)
        self.Capture.clicked.connect(self.Screen_capture)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.lcd = QLCDNumber(Dialog)
        self.lcd.display('')
        self.lcd.setDigitCount(12) # Diplay Number Limit
        self.lcd.setGeometry(QtCore.QRect(10, 10, 350, 50))

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "HARDWARE CHECK"))
        self.TimerOn.setText(_translate("Dialog", "Start"))
        self.TimerOff.setText(_translate("Dialog", "Stop"))
        self.Label_CPU.setText(_translate("Dialog", "CPU"))
        self.Label_RAM.setText(_translate("Dialog", "RAM"))
        self.Capture.setText(_translate("Dialog", "Capture"))

    def Hardware_Timer(self):
        pid = os.getpid()
        cpu_usage = psutil.cpu_percent()
        memory_usage = psutil.virtual_memory()
        self.progressBar_CPU.setValue(int(cpu_usage))
        self.progressBar_RAM.setValue(int(memory_usage.percent))

    def Timer_Start(self):
        self.Check_Timer.start()

    def Timer_Stop(self):
        self.Check_Timer.stop()

    def Display_Time(self):
        currentTime = QTime.currentTime().toString("hh:mm:ss:zzz") # zzz miliseconds
        self.lcd.display(currentTime)

    def Screen_capture(self):
        Date = QDate.currentDate().toString("yyMMdd_")
        time = QTime.currentTime().toString("hh_mm_ss")
        img=ImageGrab.grab()
        saveas="{}{}".format(Date + time,'.bmp')
        img.save(saveas)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    sys.exit(app.exec_())
