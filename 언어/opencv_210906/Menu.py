import cv2
import numpy as np
import Tensor
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
                           "QGroupBox \n"
                           "{\n"
                           "     border: 1px solid balck;\n"
                           "}\n"
                           )
        # Image 관련 변수
        self.img_url = ''
        self.img_ori  = np.zeros((100, 100), np.uint8)
        self.img_data = np.zeros((100, 100), np.uint8)
        self.img_obj = QPixmap()
        self.lb_img = QLabel()
        self.img_Threshold = 0
        self.img_ratioX = -1
        self.img_ratioY = -1

        self.grid = QGridLayout()
        self.ButtonMenu = self.ButtonGroup()

        self.ScrollArea = QScrollArea(self)
        self.ScrollArea.setStyleSheet("color:balck")
        self.ScrollArea.setWidgetResizable(True)
        self.ScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ScrollArea.setWidget(self.lb_img)

        self.grid.addWidget(self.ScrollArea, 0, 0)
        self.grid.addWidget(self.ButtonMenu, 0, 1)

        self.grid.setColumnMinimumWidth(0, 700)
        self.grid.setColumnMinimumWidth(1, 200)
        self.setLayout(self.grid)

        self.drawRoi = QRect()
        self.Sx, self.Sy = -1, -1
        self.Ex, self.Ey = -1, -1
        self.lb_img.setMouseTracking(True)

        self.Deep_Learning = Tensor.TensorFlow()

        self.show()

    def mousePressEvent(self, event):  #event : QMouseEvent
        if event.buttons() & Qt.LeftButton:
            #print('BUTTON PRESS - LEFT')
            self.Sx, self.Sy = event.x(), event.y()
        #if event.buttons() & Qt.MidButton:
            #print('BUTTON PRESS - MIDDLE')
        #if event.buttons() & Qt.RightButton:
            #print('BUTTON PRESS - RIGHT')

    def mouseMoveEvent(self, event):  # event QMouseEvent
        self.Ex, self.Ey = event.x(), event.y()
        self.draw_rectangle()

    def mouseReleaseEvent(self, event):
        self.Ex, self.Ey = event.x(), event.y()
        self.draw_rectangle()
        print('BUTTON RELEASE')

    # Mouse Callback함수 : 파라미터는 고정됨.
    def draw_rectangle(self):
        if (self.img_ratioX == -1) | (self.img_ratioY == -1):
            return

        Sx = self.Sx - 10
        Ex = self.Ex - 10
        Sy = self.Sy - 20
        Ey = self.Ey - 20

        if Ex > self.img_obj.width():
            Ex = self.img_obj.width()

        if Ey > self.img_obj.height():
            Ey = self.img_obj.height()

        self.drawRoi.left   = int((Sx * self.img_ratioX))
        self.drawRoi.right  = int((Ex * self.img_ratioX))
        self.drawRoi.top    = int(((Sy) * self.img_ratioY))
        self.drawRoi.bottom = int(((Ey) * self.img_ratioY))

        self.img_data = self.img_ori.copy()
        cv2.rectangle(self.img_data, (self.drawRoi.left, self.drawRoi.top), (self.drawRoi.right, self.drawRoi.bottom), (0, 0, 255), 3)

        self.Draw_Image(self.img_data)

    def ButtonGroup(self):
        groupbox = QGroupBox()

        grid = QGridLayout()
        self.TopGroup = self.FilterGroup()
        self.BtmGroup = self.ResultGroup()

        grid.addWidget(self.TopGroup, 0, 0)
        grid.addWidget(self.BtmGroup, 1, 0)
        self.setLayout(grid)

        groupbox.setLayout(grid)

        return groupbox

    def FilterGroup(self):
        groupbox = QGroupBox()

        self.radio1 = QRadioButton('Original')
        self.radio2 = QRadioButton('Binary Filter')
        self.radio1.setChecked(True)
        #lamda 일단 생성 후 img_data 당겨오기
        self.radio1.clicked.connect(lambda :self.Draw_Image(self.img_data))
        self.radio2.clicked.connect(self.ImageToBinary)

        self.PushBtn1 = QPushButton('Test')
        self.PushBtn1.clicked.connect(self.deep_learning_test)
        self.PushBtn2 = QPushButton('Save')
        self.PushBtn2.clicked.connect(self.deep_learning_save)
        self.PushBtn3 = QPushButton('Load')
        self.PushBtn3.clicked.connect(self.deep_learning_load)
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
    def ResultGroup(self):
        groupbox = QGroupBox()

        self.list_Result = QListWidget()
        self.list_Result.itemClicked.connect(self.result_item_click)
        self.ResultScrollArea = QScrollArea(self)
        self.ResultScrollArea.setStyleSheet("color:balck")
        self.ResultScrollArea.setWidgetResizable(True)
        self.ResultScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.ResultScrollArea.setWidget(self.list_Result)

        grid = QGridLayout()
        grid.addWidget(self.ResultScrollArea,   0, 0)

        self.setLayout(grid)

        groupbox.setLayout(grid)

        return groupbox
    def Load_Draw_Image(self, image_path):
        image_path_replaced = np.fromfile(image_path, np.uint8)
        img = cv2.imdecode(image_path_replaced, cv2.IMREAD_GRAYSCALE)

        #self.img_data = cv2.imread(image_path)
        #self.img_ori = self.img_data
        #self.binary_cv = cv2.imencode('.jpg', self.img_data)[1].tobytes()
        #self.img_obj.loadFromData(self.binary_cv)
        self.img_obj.loadFromData(image_path_replaced)
        self.img_obj = self.img_obj.scaledToWidth(700)
        self.img_obj = self.img_obj.scaledToHeight(525)
        self.lb_img.setPixmap(self.img_obj)

        imgY, imgX = img.shape
        viewX, viewY = self.img_obj.width(), self.img_obj.height()
        self.img_ratioX, self.img_ratioY = imgX / viewX, imgY / viewY
        #print(self.img_ratioX, self.img_ratioY)

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

    def deep_learning_test(self):
        # Test
        for i in range(1, 51):
            imgPath = 'D:\\KJH\\장비백업\\A3961\\Log\\IMAGE\\Test\\0 (%d).jpg' % i

            result = self.Deep_Learning.Test(imgPath)

            if(result > 0):
                self.list_Result.addItem("{} Image is TOP".format(i))
            else:
                self.list_Result.addItem("{} Image is BTM".format(i))

    def deep_learning_save(self):
        self.Deep_Learning.Save()

    def deep_learning_load(self):
        self.Deep_Learning.Load()

    def result_item_click(self, item):
        #print('!!! click {}'.format(item.text()))
        Index = item.text()
        Index_replaced = Index.split()
        imgPath = 'D:\\KJH\\장비백업\\A3961\\Log\\IMAGE\\Test\\0 (%s).jpg' % Index_replaced[0]
        self.Load_Draw_Image(imgPath)
