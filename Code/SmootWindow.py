# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SmootWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

import statistics
from scipy.ndimage import gaussian_filter1d
from numpy import pi, exp, sqrt
from copy import deepcopy
from Signal import Signals

import csv
from PyQt5 import QtCore, QtGui, QtWidgets
import matplotlib.pyplot as plt


class Ui_SmootingWindow(object):
    def setupUi(self, SmootingWindow, mainWindow):
        SmootingWindow.setObjectName("SmootingWindow")
        SmootingWindow.resize(300, 350)
        SmootingWindow.setMaximumSize(QtCore.QSize(300, 350))
        self.smoothLabel = QtWidgets.QLabel(SmootingWindow)
        self.smoothLabel.setGeometry(QtCore.QRect(45, 10, 210, 33))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.smoothLabel.setFont(font)
        self.smoothLabel.setObjectName("smoothLabel")
        self.combo = QtWidgets.QComboBox(SmootingWindow)
        self.combo.setGeometry(QtCore.QRect(21, 71, 149, 22))
        self.combo.setObjectName("combo")
        self.combo.addItem("")
        self.combo.addItem("")
        self.combo.addItem("")
        self.combo.activated.connect(self.display)  # erkana bastır
        self.stackedWidget = QtWidgets.QStackedWidget(SmootingWindow)
        self.stackedWidget.setGeometry(QtCore.QRect(20, 100, 151, 80))
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setObjectName("page_7")
        self.layoutWidget = QtWidgets.QWidget(self.page_7)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 127, 47))
        self.layoutWidget.setObjectName("layoutWidget")
        self.vbox = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.vbox.setObjectName("vbox")
        self.chooseLabel = QtWidgets.QLabel(self.layoutWidget)
        self.chooseLabel.setObjectName("chooseLabel")
        self.vbox.addWidget(self.chooseLabel)
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.setObjectName("hbox")
        self.rb3 = QtWidgets.QRadioButton(self.layoutWidget)
        self.rb3.setChecked(True)
        self.rb3.setObjectName("rb3")
        self.hbox.addWidget(self.rb3)
        self.rb5 = QtWidgets.QRadioButton(self.layoutWidget)
        self.rb5.setObjectName("rb5")
        self.hbox.addWidget(self.rb5)
        self.vbox.addLayout(self.hbox)
        self.stackedWidget.addWidget(self.page_7)
        self.page_8 = QtWidgets.QWidget()
        self.page_8.setObjectName("page_8")
        self.layoutWidget_2 = QtWidgets.QWidget(self.page_8)
        self.layoutWidget_2.setGeometry(QtCore.QRect(0, 0, 127, 47))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.vbox_2 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.vbox_2.setContentsMargins(0, 0, 0, 0)
        self.vbox_2.setObjectName("vbox_2")
        self.chooseLabel_2 = QtWidgets.QLabel(self.layoutWidget_2)
        self.chooseLabel_2.setObjectName("chooseLabel_2")
        self.vbox_2.addWidget(self.chooseLabel_2)
        self.hbox_2 = QtWidgets.QHBoxLayout()
        self.hbox_2.setObjectName("hbox_2")
        self.rb3_2 = QtWidgets.QRadioButton(self.layoutWidget_2)
        self.rb3_2.setChecked(True)
        self.rb3_2.setObjectName("rb3_2")
        self.hbox_2.addWidget(self.rb3_2)
        self.rb5_2 = QtWidgets.QRadioButton(self.layoutWidget_2)
        self.rb5_2.setObjectName("rb5_2")
        self.hbox_2.addWidget(self.rb5_2)
        self.vbox_2.addLayout(self.hbox_2)
        self.stackedWidget.addWidget(self.page_8)
        self.page_11 = QtWidgets.QWidget()
        self.page_11.setObjectName("page_11")
        self.stackedWidget.addWidget(self.page_11)
        self.showWarpButton = QtWidgets.QPushButton(SmootingWindow)
        self.showWarpButton.setGeometry(QtCore.QRect(65, 290, 170, 30))
        self.showWarpButton.setObjectName("showWarpButton")
        self.showWarpButton.setCheckable(True)
        self.retranslateUi(SmootingWindow)
        QtCore.QMetaObject.connectSlotsByName(SmootingWindow)
        self.showWarpButton.clicked.connect(lambda: self.op(SmootingWindow, mainWindow))

    def op(self, SmoothWindow, mainWindow):
        mainWindow.stack.append(self.operations(mainWindow.stack[-1].datas))
        SmoothWindow.close()
        mainWindow.plot()

    def operations(self, signals):
        n = len(signals)  # sinyal sayısı
        newsignals = list()
        index = self.combo.currentIndex()
        windowSize = self.findWindowSize(index)
        if index == 0:
            for i in range(n):
                newsignals.append(self.smoothArithmeticMean(windowSize, signals[i]))
        elif index == 1:
            for i in range(n):
                newsignals.append(self.smoothWeightedMean(windowSize, signals[i]))
        elif index == 2:
            for i in range(n):
                newsignals.append(self.smoothGaussian(signals[i]))

        return Signals(newsignals)

    def smoothArithmeticMean(self, windowSize, signal):
        # newData = [[0 for i in range(len(signals[j].data))] for j in range(len(signals))]
        n = len(signal)
        newData = [0] * n
        if (windowSize == 3):
            for j in range(1, n - 1):
                newData[j] = (signal[j - 1] + signal[j] + signal[j + 1]) // 3

            newData[0] = newData[1]
            newData[-1] = newData[-2]
        else:
            for j in range(2, n - 2):
                newData[j] = (signal[j - 2] + signal[j - 1] + signal[j] + signal[j + 1] + signal[j + 2]) // 5

            newData[0] = newData[1] = newData[2]
            newData[-1] = newData[-2] = newData[-3]

        return newData

    def smoothWeightedMean(self, windowSize, signal):
        n = len(signal)
        newData = [0] * n
        if (windowSize == 3):
            for j in range(1, n - 1):
                newData[j] = (signal[j - 1] + signal[j] * 3 + signal[j + 1]) // 5

            newData[0] = newData[1]
            newData[-1] = newData[-2]
        else:
            for j in range(2, n - 2):
                newData[j] = (signal[j - 2] + signal[j - 1] * 2 + signal[j] * 3 + signal[j + 1] * 2 + signal[j + 2]) // 5

            newData[0] = newData[1] = newData[2]
            newData[-1] = newData[-2] = newData[-3]

        return newData

    def smoothGaussian(self, signal):
        newData = gaussian_filter1d(signal, 1)
        return newData

    def display(self, i):
        self.stackedWidget.setCurrentIndex(i)
        print(str(self.findWindowSize(i)) + " is selected")

    def findWindowSize(self, i):
        windowSize = None
        if (i == 0):
            if (self.rb3.isChecked() == True):
                windowSize = 3
            else:
                windowSize = 5
        elif (i == 1):
            if (self.rb3_2.isChecked() == True):
                windowSize = 3
            else:
                windowSize = 5
        return windowSize

    def retranslateUi(self, SmootingWindow):
        _translate = QtCore.QCoreApplication.translate
        SmootingWindow.setWindowTitle(_translate("SmootingWindow", "Form"))
        self.smoothLabel.setText(_translate("SmootingWindow", "Smooth Signals"))
        self.combo.setItemText(0, _translate("SmootingWindow", "Triangle Average"))
        self.combo.setItemText(1, _translate("SmootingWindow", "Rectangular Average"))
        self.combo.setItemText(2, _translate("SmootingWindow", "Gaussian"))
        self.chooseLabel.setText(_translate("SmootingWindow", "Choose Window Size:"))
        self.rb3.setText(_translate("SmootingWindow", "3"))
        self.rb5.setText(_translate("SmootingWindow", "5"))
        self.chooseLabel_2.setText(_translate("SmootingWindow", "Choose Window Size:"))
        self.rb3_2.setText(_translate("SmootingWindow", "3"))
        self.rb5_2.setText(_translate("SmootingWindow", "5"))
        self.showWarpButton.setText(_translate("SmootingWindow", "Show Warping Methods"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    SmootingWindow = QtWidgets.QWidget()
    ui = Ui_SmootingWindow()
    ui.setupUi(SmootingWindow, s)
    SmootingWindow.show()
    sys.exit(app.exec_())
