import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtPrintSupport, QtCore

class CenterWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QWidget \n"
                           "{\n"       
	                       "     background:#FFFFFF;\n"
                           "}\n"
                           "QPushButton \n"
                           "{\n"
                           "  color:white;\n"
                           "  background : rgb(58, 134, 255);\n"
                           "  border-radius: 5;\n"
                           "}\n"
                           )
        self.img_url = ''
        self.img_data = ''
        self.img_obj = QPixmap()
        self.lb_img = QLabel()

        grid = QGridLayout()
        grid.setRowStretch(1,2)
        grid.addWidget(self.lb_img, 0, 0)
        grid.addWidget(self.ButtonGroup(), 0, 1)
        self.setLayout(grid)

        self.show()

    def ButtonGroup(self):
        groupbox = QGroupBox('Buttons')

        grid = QGridLayout()
        grid.addWidget(self.FilterGroup(), 0, 0)
        grid.addWidget(self.FilterGroup(), 1, 0)
        self.setLayout(grid)

        groupbox.setLayout(grid)

        return groupbox

    def FilterGroup(self):
        groupbox = QGroupBox('Filter Group')

        radio1 = QRadioButton('Original')
        radio2 = QRadioButton('Binary Filter')
        radio1.setChecked(True)

        PushBtn1 = QPushButton('Button 1')
        PushBtn2 = QPushButton('Button 2')
        PushBtn3 = QPushButton('Button 3')

        vbox = QVBoxLayout()
        vbox.addWidget(radio1)
        vbox.addWidget(radio2)
        vbox.addWidget(PushBtn1)
        vbox.addWidget(PushBtn2)
        vbox.addWidget(PushBtn3)

        groupbox.setLayout(vbox)

        return groupbox

    def Draw_Image(self, image):
        self.img_data = cv2.imread(image)
        self.binary_cv = cv2.imencode('.PNG', self.img_data)[1].tobytes()
        self.img_obj.loadFromData(self.binary_cv)
        self.img_obj = self.img_obj.scaledToWidth(700)
        self.lb_img.setPixmap(self.img_obj)
