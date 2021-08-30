import os
import psutil
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import QBasicTimer


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        okButton = QPushButton('OK')
        okButton.clicked.connect(self.doCheck())

        cancelButton = QPushButton('Cancel')

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(okButton)
        hbox.addWidget(cancelButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(3)
        vbox.addLayout(hbox)
        vbox.addStretch(1)

        label1 = QLabel('CPU', self)
        label1.move(20, 20)
        label2 = QLabel('GPU', self)
        label2.move(20, 60)
        label1 = QLabel('RAM', self)
        label1.move(20, 100)

        BarCPU = QProgressBar(self)
        BarCPU.setWindowTitle('QProgressBar')
        BarCPU.setGeometry(60, 20, 100, 20)
        BarCPU.setValue(0)
        BarCPU.show()

        self.setLayout(vbox)

        self.setWindowTitle('Hardware Check')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def timerEvent(self, e):
        self._check_cpu_and_memory()

        self.BarCPU.setValue(self.memory_usage)

    def _check_cpu_and_memory(self):
        pid = os.getpid()
        py = psutil.Process(pid)

        cpu_usage = os.popen("ps aux | grep " + str(pid) + " | grep -v grep | awk '{print $3}'").read()
        cpu_usage = cpu_usage.replace("\n", "")

        memory_usage = round(py.memory_info()[0] / 2. ** 30, 2)

        print("cpu usage\t\t:", cpu_usage, "%")
        print("memory usage\t\t:", memory_usage, "%")

    def doCheck(self):
        if self.timer.isActive():
            self.timer.stop()
            self.btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.btn.setText('Stop')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
