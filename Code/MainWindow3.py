# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow3.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from SmootWindow import Ui_SmootingWindow
from PTWParameters import Ui_PTWParameters
from COWParameters import Ui_COWParameters
from DTWParameters import Ui_DTWParameters
from COWFunctions import COWFunctions
from DTWFunctions import DTWFunctions
from IBAligner import IBAligner
from SCBAligner import SCBAligner
from PTWFunctions import PTWFunctions
from EvaluateWindow import Ui_Table

from plot1 import PlotCanvas
from Signal import Signals

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import csv
import os
import numpy as np
import wave
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from scipy.io import wavfile


class Ui_MainWindow(object):
    def openSmootWindow(self):
        if (len(self.stack) != 0):
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_SmootingWindow()
            self.ui.setupUi(self.window, self)
            self.window.show()
        else:
            print("No data for Smooth")

    def openEvaluateWindow(self):
        if (len(self.stack) != 0):
            self.window = QtWidgets.QWidget()
            self.ui = Ui_Table()
            self.ui.setupUi(self.window, self)
            self.window.show()
        else:
            print("No data for Evaluate")

    def openPTWWindow(self):
        if (len(self.stack) != 0):
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_PTWParameters()
            self.ui.setupUi(self.window, self)
            self.window.show()
        else:
            print("No data for PTW")

    def openCOWWindow(self):
        if (len(self.stack) != 0):
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_COWParameters()
            self.ui.setupUi(self.window, self)
            self.window.show()
        else:
            print("No data for COW")

    def openDTWWindow(self):
        if (len(self.stack) != 0):
            self.window = QtWidgets.QMainWindow()
            self.ui = Ui_DTWParameters()
            self.ui.setupUi(self.window, self)
            self.window.show()
        else:
            print("No data for DTW")

    def openFileWindow(self):
        self.stack.clear()
        path = QFileDialog.getOpenFileName(MainWindow, "Open File", "",
                                           "Tab-Seperated-Values (*.tsv);;Waveform Audio File Format (*.wav)")[0]
        if path:
            file = open(path, "r")
            if not file.readable():
                QMessageBox.warning(self, "Recent Files",
                                    "Cannot read file %s:\n%s." % (path, file.errorString()))
                return

            QApplication.setOverrideCursor(Qt.WaitCursor)
            QApplication.restoreOverrideCursor()
            self.lineEdit.setText(path)
            self.curFilePath = path
            s = os.path.splitext(os.path.basename(self.curFilePath))[1]
            b = list()
            if (s[1::] == "tsv"):
                tsvData = csv.reader(file, delimiter="\t")
                a = list(map(list, zip(*list(tsvData))))
                a = [list(map(int, lst)) for lst in a]

                for i in range(len(a)):
                    b.append(a[i])

            elif (s[1::] == "wav"):
                fs, data = wavfile.read(path)
                data = np.asmatrix(data).T
                b = np.array(data)

            self.stack.append(Signals(b))
            self.plot()
            file.close()
            MainWindow.statusBar().showMessage("File loaded", 2000)

    def saveAsText(self):
        if self.curFilePath:
            filename = os.path.splitext(os.path.basename(self.curFilePath))[0] + ".txt"
            file = open(filename, "w")
            fileWriter = csv.writer(file, delimiter="\t")
            datas = [data for data in self.stack[-1].datas]
            datas = list(map(list, zip(*list(datas))))
            datas = [list(map(int, lst)) for lst in datas]
            print(len(datas[0]))
            for row in datas:
                fileWriter.writerow(row)

            MainWindow.statusBar().showMessage("File saved", 2000)
            file.close()

    def clearPanel(self):
        self.stack.clear()
        if (len(self.widgets) != 0):
            for i in range(len(self.widgets)):
                self.widgets[i].clear()
            self.widgets.clear()
            for i in reversed(range(self.gridLayout_2.count())):
                self.gridLayout_2.itemAt(i).widget().setParent(None)

    def undo(self):
        if len(self.stack) > 1:
            self.stack.pop()
            self.plot()
        else:
            print("There is no data for Undo")

    def undoAll(self):
        if (len(self.stack) > 1):
            tmp = self.stack[0]
            self.stack.clear()
            self.stack.append(tmp)
            self.plot()
        else:
            print("Already no change in data")

    def enhancement(self):  # 2.dereceden türev
        if len(self.stack) != 0:
            datas = [np.array(sig, dtype=np.int64) for sig in self.stack[-1].datas]
            newData = [np.diff(data, n=2) for data in datas]  # 2.türev

            for i in range(len(datas)):
                for j in range(2, len(datas[i])):
                    newData[i][j - 2] = datas[i][j] - newData[i][j - 2]

            self.stack.append(Signals(newData))
            self.plot()
        else:
            print("There is no data for Enhancement")

    def baseline(self):
        if len(self.stack) != 0:
            datas = [np.array(sig) for sig in self.stack[-1].datas]
            windowSize = 36
            newData = list()
            m = list()
            for i in range(len(datas)):
                for j in range(0, len(datas[i]) - windowSize, windowSize):
                    m.append(min(datas[i][j:j + windowSize]))
                m.append(min(datas[i][j:]))
                k = 0
                for j in range(0, len(datas[i]) - windowSize, windowSize):
                    datas[i][j:j + windowSize] -= m[k]
                    k += 1
                datas[i][j:] -= m[k]
                newData.append(datas[i])

            self.stack.append(Signals(newData))
            self.plot()
        else:
            print("There is no data for Baseline Correction")

    def plot(self, index=None):
        if (len(self.stack) == 0):
            print("There is no data")
            return
        if (len(self.widgets) != 0):
            for i in range(len(self.widgets)):
                self.widgets[i].clear()
            self.widgets.clear()
            for i in reversed(range(self.gridLayout_2.count())):
                self.gridLayout_2.itemAt(i).widget().setParent(None)
        signals = self.stack[-1].datas
        n = len(signals)

        if (self.actionShow_Signals_On_Seperate_Axes.isChecked()):  # seperate
            if index is not None:  # seperate aligned plot ise
                for i in range(n):
                    if (i != index):
                        self.widgets.append(PlotCanvas(self.scrollAreaWidgetContents))
                        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                        sizePolicy.setHorizontalStretch(0)
                        sizePolicy.setVerticalStretch(0)
                        sizePolicy.setHeightForWidth(self.widgets[-1].sizePolicy().hasHeightForWidth())
                        self.widgets[-1].setSizePolicy(sizePolicy)
                        self.widgets[-1].setMinimumSize(QtCore.QSize(900, 300))
                        self.widgets[-1].plotNew(signals[index], signals[i])
                        self.gridLayout_2.addWidget(self.widgets[-1], i, 0, 1, 1)
            else:  # seperate plot
                for i in range(n):
                    self.widgets.append(PlotCanvas(self.scrollAreaWidgetContents))
                    sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(self.widgets[-1].sizePolicy().hasHeightForWidth())
                    self.widgets[-1].setSizePolicy(sizePolicy)
                    self.widgets[-1].setMinimumSize(QtCore.QSize(900, 300))
                    self.widgets[-1].plotNew(signals[i])
                    self.gridLayout_2.addWidget(self.widgets[-1], i, 0, 1, 1)
        else:
            self.widgets.append(PlotCanvas(self.scrollAreaWidgetContents))
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.widgets[-1].sizePolicy().hasHeightForWidth())
            self.widgets[-1].setSizePolicy(sizePolicy)
            self.widgets[-1].setMinimumSize(QtCore.QSize(900, 300))
            self.gridLayout_2.addWidget(self.widgets[-1], 0, 0, 1, 1)
            if index is not None:  # single aligned plot ise
                self.widgets[-1].plotNew(signals[0], signals[1])
            else:  # single plot
                for i in range(n):
                    self.widgets[-1].plotNew(signals[i])

    def plotWarpedSegment(self, index, lines):
        if (len(self.widgets) != 0):
            for i in range(len(self.widgets)):
                self.widgets[i].clear()
            self.widgets.clear()
            for i in reversed(range(self.gridLayout_2.count())):
                self.gridLayout_2.itemAt(i).widget().setParent(None)
        signals = self.stack[-1].datas
        n = len(signals)
        for i in range(n):
            if (i != index):
                self.widgets.append(PlotCanvas(self.scrollAreaWidgetContents))
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(self.widgets[-1].sizePolicy().hasHeightForWidth())
                self.widgets[-1].setSizePolicy(sizePolicy)
                self.widgets[-1].setMinimumSize(QtCore.QSize(900, 300))
                self.widgets[-1].plotWarpedSegments(signals[index], signals[i], lines[i])
                self.gridLayout_2.addWidget(self.widgets[-1], i, 0, 1, 1)

    def evaluateDTW(self):
        signals = self.stack[-1].datas
        signal1 = signals[0]
        signal2 = signals[1]

        dtwResult = [None] * 4  # 0 corr,1 rms,2 peakmatch , 3 time
        dtw = DTWFunctions(signal1, 3, 0, 0)  # signal1, gap, n, T
        dtw.updateSignal2(signal2)

        t0 = time.time()
        dtwAligned = dtw.getAlignedSignal(dtw.getWarpedPath())
        t1 = time.time()

        dtwRMS = 0
        dtwRMS = np.float64(dtwRMS)
        for i in range(len(signal1)):
            dtwRMS += (signal1[i] - dtwAligned[i]) ** 2
        dtwRMS /= len(signal1)
        dtwRMS = dtwRMS ** 0.5

        dtwResult[0] = round((np.corrcoef(signal1, dtwAligned))[0][1], 2)
        dtwResult[1] = round(dtwRMS, 2)
        dtwResult[2] = round(self.peakMatchSimilarity(signal1, dtwAligned), 2)
        dtwResult[3] = round(t1 - t0, 2)

        print(dtwResult)
        return dtwResult

    def evaluateCOW(self):
        signals = self.stack[-1].datas
        signal1 = signals[0]
        signal2 = signals[1]

        cowResult = [None] * 4
        cow = COWFunctions(signal1, 10, 3)  # segment , slack
        cow.updateSignal2(signal2)
        t0 = time.time()
        cowAlignedsignal = cow.getAlignedSignals(cow.getWarpedSegments())
        t1 = time.time()
        cowRMS = 0
        cowRMS = np.float64(cowRMS)
        for i in range(len(signal1)):
            cowRMS += (signal1[i] - cowAlignedsignal[i]) ** 2
        cowRMS /= len(signal1)
        cowRMS = cowRMS ** 0.5

        cowResult[0] = round((np.corrcoef(signal1, cowAlignedsignal))[0][1], 2)
        cowResult[1] = round(cowRMS, 2)
        cowResult[2] = round(self.peakMatchSimilarity(signal1, cowAlignedsignal), 2)
        cowResult[3] = round(t1 - t0, 2)

        print(cowResult)
        return cowResult

    def evaluatePTW(self):
        signals = self.stack[-1].datas
        signal1 = np.asarray(signals[0])
        signal2 = np.asarray(signals[1])

        ptwResults = [None] * 4
        ptw = PTWFunctions(signal1, False, 1e-5, 10,[0, 1, 0])  # signal1, isSmooth, delta, gap, warpingFunctions
        ptw.updateSignal2(signal2)
        t0 = time.time()
        ptwAligned = ptw.getWarpedSignals()
        t1 = time.time()
        ptwRMS = 0
        ptwRMS = np.float64(ptwRMS)
        for i in range(len(signal1)):
            ptwRMS += (signal1[i] - ptwAligned[i]) ** 2
        ptwRMS /= len(signal1)
        ptwRMS = np.sqrt(ptwRMS)
        ptwResults[0] = round((np.corrcoef(signal1, ptwAligned))[0][1], 2)
        ptwResults[1] = round(ptwRMS, 2)
        ptwResults[2] = round(self.peakMatchSimilarity(signal1, ptwAligned), 2)
        ptwResults[3] = round(t1 - t0, 2)

        print(ptwResults)
        return ptwResults

    def evaluateOriginal(self):
        signals = self.stack[-1].datas
        signal1 = np.asarray(signals[0])
        signal2 = np.asarray(signals[1])

        originalResult = [None] * 2
        orRMS = 0
        orRMS = np.int64(orRMS)
        for i in range(len(signal1)):
            orRMS += pow((signal1[i] - signal2[i]), 2)
        orRMS /= len(signal1)
        orRMS = orRMS ** 0.5
        originalResult[0] = round((np.corrcoef(signal1, signal2))[0][1], 2)
        originalResult[1] = round(orRMS, 2)

        print(originalResult)
        return originalResult

    def evaluateAllMethods(self):
        self.evaluateOriginal()
        self.evaluateDTW()
        self.evaluatePTW()
        self.evaluateCOW()

    def peakMatchSimilarity(self, s1, s2):
        a1 = list()
        a2 = list()
        signal1 = np.zeros(len(s1), dtype=np.float64)
        signal2 = np.zeros(len(s2), dtype=np.float64)

        for j in range(1, len(s1) - 1):
            signal1[j] = s1[j - 1] * 0.2 + s1[j] * 0.6 + s1[j + 1] * 0.2
            signal2[j] = s2[j - 1] * 0.2 + s2[j] * 0.6 + s2[j + 1] * 0.2
        signal1[0] = signal1[1]
        signal1[-1] = signal1[-2]
        signal2[0] = signal2[1]
        signal2[-1] = signal2[-2]

        for i in range(1, len(signal1) - 2):
            if (signal1[i] > signal1[i - 1] and signal1[i] > signal1[i + 1]):
                a1.append(i)
            if (signal2[i] > signal2[i - 1] and signal2[i] > signal2[i + 1]):
                a2.append(i)
        m = min(len(a1), len(a2))
        matching = 0
        for i in range(m):
            if (a1[i] in a2):
                matching += 1

        return (matching / m) * 100 if m != 0 else 0

    def setupUi(self, MainWindow):
        self.curFilePath = None
        self.stack = list()  # sinyalleri bir bütün olarak  -->1.Sinyaller topluluğu ,2.,3. ,...
        self.widgets = list()
        self.window = None
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 600)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setInputMethodHints(QtCore.Qt.ImhNone)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(10, 10, 10, 10)
        self.gridLayout.setSpacing(5)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.openButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.openButton.sizePolicy().hasHeightForWidth())
        self.openButton.setSizePolicy(sizePolicy)
        self.openButton.setMaximumSize(QtCore.QSize(57, 33))
        self.openButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/document-new.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.openButton.setIcon(icon)
        self.openButton.setObjectName("openButton")
        self.openButton.clicked.connect(self.openFileWindow)
        self.horizontalLayout.addWidget(self.openButton)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveButton.sizePolicy().hasHeightForWidth())
        self.saveButton.setSizePolicy(sizePolicy)
        self.saveButton.setMaximumSize(QtCore.QSize(57, 33))
        self.saveButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/document_save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon1)
        self.saveButton.setObjectName("saveButton")
        self.saveButton.clicked.connect(self.saveAsText)
        self.horizontalLayout.addWidget(self.saveButton)
        self.undoButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.undoButton.sizePolicy().hasHeightForWidth())
        self.undoButton.setSizePolicy(sizePolicy)
        self.undoButton.setMaximumSize(QtCore.QSize(57, 33))
        self.undoButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("Images/Trash.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.undoButton.setIcon(icon2)
        self.undoButton.setObjectName("undoButton")
        self.undoButton.clicked.connect(self.undo)
        self.horizontalLayout.addWidget(self.undoButton)
        self.clearButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clearButton.sizePolicy().hasHeightForWidth())
        self.clearButton.setSizePolicy(sizePolicy)
        self.clearButton.setMaximumSize(QtCore.QSize(57, 33))
        self.clearButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("Images/edit-clear.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearButton.setIcon(icon3)
        self.clearButton.setObjectName("clearButton")
        self.clearButton.clicked.connect(self.clearPanel)
        self.horizontalLayout.addWidget(self.clearButton)
        self.manualButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.manualButton.sizePolicy().hasHeightForWidth())
        self.manualButton.setSizePolicy(sizePolicy)
        self.manualButton.setMaximumSize(QtCore.QSize(57, 33))
        self.manualButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("Images/manual.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.manualButton.setIcon(icon4)
        self.manualButton.setObjectName("manualButton")
        self.horizontalLayout.addWidget(self.manualButton)
        self.viewButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.viewButton.sizePolicy().hasHeightForWidth())
        self.viewButton.setSizePolicy(sizePolicy)
        self.viewButton.setMaximumSize(QtCore.QSize(57, 33))
        self.viewButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("Images/view-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.viewButton.setIcon(icon5)
        self.viewButton.setObjectName("viewButton")
        self.horizontalLayout.addWidget(self.viewButton)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.labelFile = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFile.sizePolicy().hasHeightForWidth())
        self.labelFile.setSizePolicy(sizePolicy)
        self.labelFile.setMinimumSize(QtCore.QSize(400, 18))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.labelFile.setFont(font)
        self.labelFile.setObjectName("labelFile")
        self.verticalLayout.addWidget(self.labelFile)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(400, 20))
        self.lineEdit.setMaximumSize(QtCore.QSize(400, 20))
        self.lineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setAutoFillBackground(True)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 1157, 615))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setContentsMargins(15, 5, 15, 5)
        self.gridLayout_2.setSpacing(5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1200, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuPreprocessing = QtWidgets.QMenu(self.menubar)
        self.menuPreprocessing.setObjectName("menuPreprocessing")
        self.menuWarping = QtWidgets.QMenu(self.menubar)
        self.menuWarping.setObjectName("menuWarping")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionOpen.setShortcutVisibleInContextMenu(True)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(self.openFileWindow)
        self.actionSave_As_Text = QtWidgets.QAction(MainWindow)
        self.actionSave_As_Text.setShortcutVisibleInContextMenu(True)
        self.actionSave_As_Text.setObjectName("actionSave_As_Text")
        self.actionSave_As_Text.triggered.connect(self.saveAsText)
        self.actionSave_All_Results = QtWidgets.QAction(MainWindow)
        self.actionSave_All_Results.setShortcutVisibleInContextMenu(True)
        self.actionSave_All_Results.setObjectName("actionSave_All_Results")
        self.actionUndo_All_Changes = QtWidgets.QAction(MainWindow)
        self.actionUndo_All_Changes.setShortcutVisibleInContextMenu(True)
        self.actionUndo_All_Changes.setObjectName("actionUndo_All_Changes")
        self.actionUndo_All_Changes.triggered.connect(self.undoAll)
        self.actionClear_Panels = QtWidgets.QAction(MainWindow)
        self.actionClear_Panels.setMenuRole(QtWidgets.QAction.TextHeuristicRole)
        self.actionClear_Panels.setShortcutVisibleInContextMenu(True)
        self.actionClear_Panels.setObjectName("actionClear_Panels")
        self.actionClear_Panels.triggered.connect(self.clearPanel)
        self.actionShow_Signals_On_Single_Axis = QtWidgets.QAction(MainWindow)
        self.actionShow_Signals_On_Single_Axis.setCheckable(True)
        self.actionShow_Signals_On_Single_Axis.setShortcut("")
        self.actionShow_Signals_On_Single_Axis.setShortcutVisibleInContextMenu(True)
        self.actionShow_Signals_On_Single_Axis.setObjectName("actionShow_Signals_On_Single_Axis")
        self.actionShow_Signals_On_Single_Axis.triggered.connect(
            lambda: self.actionShow_Signals_On_Seperate_Axes.setChecked(False))
        self.actionShow_Signals_On_Single_Axis.triggered.connect(lambda: self.plot(None))
        self.actionShow_Signals_On_Seperate_Axes = QtWidgets.QAction(MainWindow)
        self.actionShow_Signals_On_Seperate_Axes.setCheckable(True)
        self.actionShow_Signals_On_Seperate_Axes.setShortcutVisibleInContextMenu(True)
        self.actionShow_Signals_On_Seperate_Axes.setObjectName("actionShow_Signals_On_Seperate_Axes")
        self.actionShow_Signals_On_Seperate_Axes.triggered.connect(
            lambda: self.actionShow_Signals_On_Single_Axis.setChecked(False))
        self.actionShow_Signals_On_Seperate_Axes.triggered.connect(lambda: self.plot(None))
        self.actionSmooting = QtWidgets.QAction(MainWindow)
        self.actionSmooting.setObjectName("actionSmooting")
        self.actionSmooting.triggered.connect(self.openSmootWindow)
        self.actionResolution_Enhancement = QtWidgets.QAction(MainWindow)
        self.actionResolution_Enhancement.setObjectName("actionResolution_Enhancement")
        self.actionResolution_Enhancement.triggered.connect(self.enhancement)
        self.actionBaseline_Adjustment = QtWidgets.QAction(MainWindow)
        self.actionBaseline_Adjustment.setObjectName("actionBaseline_Adjustment")
        self.actionBaseline_Adjustment.triggered.connect(self.baseline)
        self.actionDynamic_Time_Warping = QtWidgets.QAction(MainWindow)
        self.actionDynamic_Time_Warping.setShortcutVisibleInContextMenu(True)
        self.actionDynamic_Time_Warping.setObjectName("actionDynamic_Time_Warping")
        self.actionDynamic_Time_Warping.triggered.connect(self.openDTWWindow)
        self.actionCOW = QtWidgets.QAction(MainWindow)
        self.actionCOW.setShortcutVisibleInContextMenu(True)
        self.actionCOW.setObjectName("actionCOW")
        self.actionCOW.triggered.connect(self.openCOWWindow)
        self.actionPTW = QtWidgets.QAction(MainWindow)
        self.actionPTW.setShortcutVisibleInContextMenu(True)
        self.actionPTW.setObjectName("actionPTW")
        self.actionPTW.triggered.connect(self.openPTWWindow)
        self.actionEvaluate_Warping_Methods = QtWidgets.QAction(MainWindow)
        self.actionEvaluate_Warping_Methods.setShortcutVisibleInContextMenu(True)
        self.actionEvaluate_Warping_Methods.setObjectName("actionEvaluate_Warping_Methods")
        self.actionEvaluate_Warping_Methods.triggered.connect(self.openEvaluateWindow)
        self.actionUser_Manual = QtWidgets.QAction(MainWindow)
        self.actionUser_Manual.setShortcutVisibleInContextMenu(True)
        self.actionUser_Manual.setObjectName("actionUser_Manual")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setShortcutVisibleInContextMenu(True)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave_As_Text)
        self.menuFile.addAction(self.actionSave_All_Results)
        self.menuEdit.addAction(self.actionUndo_All_Changes)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionClear_Panels)
        self.menuView.addAction(self.actionShow_Signals_On_Single_Axis)
        self.menuView.addSeparator()
        self.menuView.addAction(self.actionShow_Signals_On_Seperate_Axes)
        self.menuPreprocessing.addAction(self.actionSmooting)
        self.menuPreprocessing.addSeparator()
        self.menuPreprocessing.addAction(self.actionResolution_Enhancement)
        self.menuPreprocessing.addAction(self.actionBaseline_Adjustment)
        self.menuWarping.addAction(self.actionDynamic_Time_Warping)
        self.menuWarping.addAction(self.actionCOW)
        self.menuWarping.addAction(self.actionPTW)
        self.menuWarping.addSeparator()
        self.menuWarping.addAction(self.actionEvaluate_Warping_Methods)
        self.menuHelp.addAction(self.actionUser_Manual)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuPreprocessing.menuAction())
        self.menubar.addAction(self.menuWarping.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.labelFile.setText(_translate("MainWindow", "File:"))
        self.label.setText(_translate("MainWindow", "Signals"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuPreprocessing.setTitle(_translate("MainWindow", "Preprocessing"))
        self.menuWarping.setTitle(_translate("MainWindow", "Warping"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionOpen.setText(_translate("MainWindow", "Open File"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionSave_As_Text.setText(_translate("MainWindow", "Save As Text"))
        self.actionSave_As_Text.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_All_Results.setText(_translate("MainWindow", "Save All Results"))
        self.actionSave_All_Results.setShortcut(_translate("MainWindow", "Ctrl+Alt+ß"))
        self.actionUndo_All_Changes.setText(_translate("MainWindow", "Undo All Changes"))
        self.actionUndo_All_Changes.setShortcut(_translate("MainWindow", "Shift+U"))
        self.actionClear_Panels.setText(_translate("MainWindow", "Clear Panels"))
        self.actionShow_Signals_On_Single_Axis.setText(_translate("MainWindow", "Show Signals On Single Axis"))
        self.actionShow_Signals_On_Seperate_Axes.setText(_translate("MainWindow", "Show Signals On Seperate Axes"))
        self.actionSmooting.setText(_translate("MainWindow", "Smooting"))
        self.actionResolution_Enhancement.setText(_translate("MainWindow", "Resolution Enhancement"))
        self.actionBaseline_Adjustment.setText(_translate("MainWindow", "Baseline Adjustment"))
        self.actionDynamic_Time_Warping.setText(_translate("MainWindow", "Dynamic Time Warping"))
        self.actionDynamic_Time_Warping.setShortcut(_translate("MainWindow", "Ctrl+Shift+D"))
        self.actionCOW.setText(_translate("MainWindow", "COW"))
        self.actionCOW.setShortcut(_translate("MainWindow", "Ctrl+Shift+C"))
        self.actionPTW.setText(_translate("MainWindow", "PTW"))
        self.actionPTW.setShortcut(_translate("MainWindow", "Ctrl+Shift+P"))
        self.actionEvaluate_Warping_Methods.setText(_translate("MainWindow", "Evaluate Warping Methods"))
        self.actionEvaluate_Warping_Methods.setShortcut(_translate("MainWindow", "Ctrl+Shift+E"))
        self.actionUser_Manual.setText(_translate("MainWindow", "User Manual"))
        self.actionUser_Manual.setShortcut(_translate("MainWindow", "Shift+M"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Shift+A"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
