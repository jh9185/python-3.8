import cv2
import numpy as np
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
                           "  padding: 12;\n"
                           "  border-radius: 5;\n"
                           "}\n"
                           )

        # Image 관련 변수
        self.img_url = ''
        self.img_data = np.zeros((100, 100), np.uint8)
        self.img_obj = QPixmap()
        self.lb_img = QLabel()
        self.img_Threshold = 0

        self.grid = QGridLayout()
        self.ButtonMenu = self.ButtonGroup()

        self.grid.addWidget(self.lb_img, 0, 0)
        self.grid.addWidget(self.ButtonMenu, 0, 1)

        self.grid.setColumnMinimumWidth(0, 700)
        self.grid.setColumnMinimumWidth(1, 200)
        self.setLayout(self.grid)

        self.show()

    def ButtonGroup(self):
        groupbox = QGroupBox('Buttons')

        grid = QGridLayout()
        self.TopGroup = self.FilterGroup()
        self.BtmGroup = QLabel()

        grid.addWidget(self.TopGroup, 0, 0)
        grid.addWidget(self.BtmGroup, 1, 0)
        self.setLayout(grid)

        groupbox.setLayout(grid)

        return groupbox

    def FilterGroup(self):
        groupbox = QGroupBox('Filter Group')

        self.radio1 = QRadioButton('Original')
        self.radio2 = QRadioButton('Binary Filter')
        self.radio1.setChecked(True)
        #lamda 일단 생성 후 img_data 당겨오기
        self.radio1.clicked.connect(lambda :self.Draw_Image(self.img_data))
        self.radio2.clicked.connect(self.ImageToBinary)

        self.PushBtn1 = QPushButton('Button 1')
        self.PushBtn2 = QPushButton('Button 2')
        self.PushBtn3 = QPushButton('Button 3')
        self.PushBtn4 = QPushButton('Button 4')

        self.label_Threshold = QLabel()
        self.label_Threshold.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label_Threshold.setText(str(0))

        self.vSlider = QSlider()
        self.vSlider.setRange(0, 255)
        self.vSlider.setTickInterval(10)
        self.vSlider.setGeometry(0, 0, 30, 150)
        self.vSlider.valueChanged.connect(self.Slider_value_changed)

        grid = QGridLayout()
        grid.addWidget(self.radio1,   0, 0)
        grid.addWidget(self.radio2,   1, 0)
        grid.addWidget(self.PushBtn1, 2, 0)
        grid.addWidget(self.PushBtn2, 3, 0)
        grid.addWidget(self.PushBtn3, 4, 0)
        grid.addWidget(self.label_Threshold, 1, 1)
        grid.addWidget(self.vSlider, 1, 2, -1, 1)

        self.setLayout(grid)

        groupbox.setLayout(grid)

        return groupbox

    def Load_Draw_Image(self, image_path):
        self.img_data = cv2.imread(image_path)
        self.binary_cv = cv2.imencode('.PNG', self.img_data)[1].tobytes()
        self.img_obj.loadFromData(self.binary_cv)
        self.img_obj = self.img_obj.scaledToWidth(700)
        self.lb_img.setPixmap(self.img_obj)

    def Draw_Image(self, image):
        self.binary_cv = cv2.imencode('.bmp', image)[1].tobytes()
        self.img_obj.loadFromData(self.binary_cv)
        self.img_obj = self.img_obj.scaledToWidth(700)
        self.lb_img.setPixmap(self.img_obj)

    def ImageToBinary(self):
        img_Binary = np.zeros((100, 100), np.uint8)
        if self.img_data is None:
            QMessageBox.information(self, "Image Viewer",
                                              "Cannot load Image.")
            return
        else:
            img_Binary = self.img_data.copy()
            cv2.threshold(self.img_data, self.img_Threshold, 255, cv2.THRESH_BINARY, img_Binary)

        self.Draw_Image(img_Binary)

    def Slider_value_changed(self, value):
        if self.radio2.isChecked():
            self.label_Threshold.setText(str(value))
            self.img_Threshold = value
            self.ImageToBinary()