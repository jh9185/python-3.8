import sys
import Menu
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtPrintSupport, QtCore

class Qpixmap_App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("/* 가운데 위젯 */\n"
                           "QWidget \n"
                           "{\n"       
	                       "     background:#FFFFFF;\n"
                           "}\n"
                           "/* 메인 메뉴 */\n"
                           "QMenuBar \n"
                           "{\n"
                           "    /* 메뉴 막대 항목 사이의 간격 */\n"
                           "    spacing: 0px; \n"
                           "\n"
                           "    background: #000000;\n"
                           "}\n"
                           "\n"
                           "/* 메인 메뉴 아이템 */\n"
                           "QMenuBar::item \n"
                           "{\n"
                           "    /* box model : margin - border - padding */\n"
                           "    margin: 0px 0px 0px 0px;\n"
                           "    border-radius: 0px;\n"
                           "    padding: 12px 24px;\n"
                           "\n"
                           "    background: #000000;\n"
                           "    color: #E1E1E1;\n"
                           "\n"
                           "    font-family: Inter;\n"
                           "    font-size: 12px;\n"
                           "}\n"
                           "\n"
                           "QMenuBar::item:selected \n"
                           "{ \n"
                           "    background: #2D45EA;\n"
                           "}\n"
                           "\n"
                           "QMenuBar::item:hover \n"
                           "{\n"
                           "    background: #2D45EA;\n"
                           "}\n"
                           "\n"
                           "/* 메뉴 전체 */\n"
                           "QMenu \n"
                           "{\n"
                           "    /* 메뉴 주위에 약간의 간격 */\n"
                           "    /* box model : margin - border - padding */\n"
                           "    margin: 0px 0px; \n"
                           "    border: 0px 0px;\n"
                           "    padding: 0px 0px;\n"
                           "\n"
                           "    background: #222222;\n"
                           "}\n"
                           "\n"
                           "QMenuBar::separator \n"
                           "{\n"
                           "    width: 176px;\n"
                           "    height: 1px;\n"
                           "\n"
                           "    /* box model : margin - border - padding */\n"
                           "    margin: 5px 0px;\n"
                           "    border: 0px 0px;\n"
                           "    padding: 0px 0px;\n"
                           "\n"
                           "    background: #333333;;\n"
                           "}\n"
                           "\n"
                           "QMenuBar::indicator \n"
                           "{\n"
                           "    width: 13px;\n"
                           "    height: 13px;\n"
                           "}\n"
                           "\n"
                           "/* 메뉴 아이템 */\n"
                           "QMenu::item \n"
                           "{\n"
                           "    width: 176px;\n"
                           "    height: 19px;\n"
                           "\n"
                           "    /* box model : margin - border - padding */\n"
                           "    margin: 0px 0px;\n"
                           "    border: 0px solid transparent;\n"
                           "    padding: 4px 16px;\n"
                           "\n"
                           "    background: #222222;\n"
                           "    color: #FFFFFF;\n"
                           "\n"
                           "    font-family: Inter;\n"
                           "    font-style: normal;\n"
                           "    font-weight: normal;\n"
                           "    font-size: 11px;\n"
                           "}\n"
                           "\n"
                           "QMenu::item:!enabled \n"
                           "{\n"
                           "    color: #555555;\n"
                           "}\n"
                           "\n"
                           "QMenu::item:enabled \n"
                           "{\n"
                           "    color: #FFFFFF;\n"
                           "}\n"
                           "\n"
                           "QMenu::item:selected \n"
                           "{\n"
                           "    background: #2D45EA;\n"
                           "}\n"
                           "\n"
                           "QMenu::icon:checked \n"
                           "{ \n"
                           "}\n"
                           "")
        self.initUI()
        self.createActions()
        self.createMenus()

        self.setWindowTitle('Image Viewer')
        self.move(100, 100)

    def initUI(self):
        self.CenterImage = Menu.CenterWidget()
        self.setCentralWidget(self.CenterImage)

        self.menu_widget = self.CenterImage

        self.setGeometry(10, 10, 1000, 600)
        self.show()

    def open(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File",
                                                     QtCore.QDir.currentPath())
        if fileName[0]:
            image = QImage(fileName[0])
            if image.isNull():
                QMessageBox.information(self, "Image Viewer",
                                              "Cannot load %s." % fileName[0])
                return

            self.CenterImage.Load_Draw_Image(fileName[0])

    def createActions(self):
        self.openAct = QAction("&Open...", self, shortcut="Ctrl+O",
                                     triggered=self.open)

        self.exitAct = QAction("E&xit", self, shortcut="Ctrl+Q",
                                     triggered=self.close)

    def createMenus(self):
        self.fileMenu = QMenu("&File", self)
        self.fileMenu.addAction(self.openAct)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.exitAct)

        self.ZoomMenu = QMenu("&Zoom", self)
        #self.ZoomMenu.addAction(self.ZoomIn)
        self.ZoomMenu.addSeparator()
        #self.ZoomMenu.addAction(self.ZoomOut)
        self.ZoomMenu.addSeparator()

        self.menuBar().addMenu(self.fileMenu)
        self.menuBar().addMenu(self.ZoomMenu)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ax = Qpixmap_App()
    sys.exit(app.exec_())