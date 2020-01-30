# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'COWParameters.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from COWFunctions import COWFunctions
from Signal import Signals
import time

class Ui_COWParameters(object):
    def setupUi(self, COWParameters, mainWindow):
        signals = mainWindow.stack[-1].datas
        if len(signals) <= 2:
            mainWindow.actionShow_Signals_On_Seperate_Axes.setChecked(False)
        else:
            mainWindow.actionShow_Signals_On_Seperate_Axes.setChecked(True)

        global index
        global cow
        index = None
        cow = None
        COWParameters.setObjectName("COWParameters")
        COWParameters.resize(400, 200)
        COWParameters.setMinimumSize(QtCore.QSize(400, 200))
        COWParameters.setMaximumSize(QtCore.QSize(400, 200))
        self.COWLabel = QtWidgets.QLabel(COWParameters)
        self.COWLabel.setGeometry(QtCore.QRect(85, 15, 240, 30))
        self.COWLabel.setMaximumSize(QtCore.QSize(240, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.COWLabel.setFont(font)
        self.COWLabel.setObjectName("COWLabel")
        self.widget = QtWidgets.QWidget(COWParameters)
        self.widget.setGeometry(QtCore.QRect(20, 150, 361, 30))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.showSegmentButton = QtWidgets.QPushButton(self.widget)
        self.showSegmentButton.setObjectName("showSegmentButton")
        self.horizontalLayout_2.addWidget(self.showSegmentButton)
        self.alignProfilesButton = QtWidgets.QPushButton(self.widget)
        self.alignProfilesButton.setEnabled(False)
        self.alignProfilesButton.setObjectName("alignProfilesButton")
        self.horizontalLayout_2.addWidget(self.alignProfilesButton)
        self.undoAlignButton = QtWidgets.QPushButton(self.widget)
        self.undoAlignButton.setEnabled(False)
        self.undoAlignButton.setObjectName("undoAlignButton")
        self.horizontalLayout_2.addWidget(self.undoAlignButton)
        self.widget1 = QtWidgets.QWidget(COWParameters)
        self.widget1.setGeometry(QtCore.QRect(30, 70, 100, 47))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.refProfileLabel = QtWidgets.QLabel(self.widget1)
        self.refProfileLabel.setObjectName("refProfileLabel")
        self.verticalLayout_3.addWidget(self.refProfileLabel)
        self.combo = QtWidgets.QComboBox(self.widget1)
        self.combo.setObjectName("combo")

        self.comboUpdate(mainWindow)  ###!!!!!

        self.verticalLayout_3.addWidget(self.combo)
        self.widget2 = QtWidgets.QWidget(COWParameters)
        self.widget2.setGeometry(QtCore.QRect(160, 70, 95, 45))
        self.widget2.setObjectName("widget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.segmentLengthLabel = QtWidgets.QLabel(self.widget2)
        self.segmentLengthLabel.setObjectName("segmentLengthLabel")
        self.verticalLayout_2.addWidget(self.segmentLengthLabel)
        self.segmentLengthLineEdit = QtWidgets.QLineEdit(self.widget2)
        self.segmentLengthLineEdit.setMaximumSize(QtCore.QSize(40, 20))
        self.segmentLengthLineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.segmentLengthLineEdit.setObjectName("segmentLengthLineEdit")
        self.verticalLayout_2.addWidget(self.segmentLengthLineEdit)
        self.widget3 = QtWidgets.QWidget(COWParameters)
        self.widget3.setGeometry(QtCore.QRect(290, 70, 81, 45))
        self.widget3.setObjectName("widget3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget3)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.slackLabel = QtWidgets.QLabel(self.widget3)
        self.slackLabel.setObjectName("slackLabel")
        self.verticalLayout.addWidget(self.slackLabel)
        self.slackLineEdit = QtWidgets.QLineEdit(self.widget3)
        self.slackLineEdit.setMaximumSize(QtCore.QSize(40, 20))
        self.slackLineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.slackLineEdit.setObjectName("slackLineEdit")
        self.verticalLayout.addWidget(self.slackLineEdit)

        warpedSegments = [None] * (len(signals))

        self.showSegmentButton.clicked.connect(lambda: self.showWarpingPath(warpedSegments, mainWindow))
        self.alignProfilesButton.clicked.connect(lambda: self.alignOperation(warpedSegments, mainWindow))
        self.undoAlignButton.clicked.connect(lambda: self.undo(mainWindow))

        self.retranslateUi(COWParameters)
        QtCore.QMetaObject.connectSlotsByName(COWParameters)

    def showWarpingPath(self, warpedSegments, mainWindow):
        global index
        global cow
        t0 = time.time()
        index = self.combo.currentIndex()
        slack = int(self.slackLineEdit.text())
        segmentLength = int(self.segmentLengthLineEdit.text())
        signals = mainWindow.stack[-1].datas
        cow = COWFunctions(signals[index], segmentLength, slack)
        lines = list()
        for i in range(len(signals)):
            if (i != index):
                cow.updateSignal2(signals[i])
                warpedSegments[i] = cow.getWarpedSegments()
                lines.append(cow.forPlotWarpedSegments(warpedSegments[i]))
            else:
                lines.append(None)

        mainWindow.plotWarpedSegment(index, lines)
        t1= time.time()
        print(t1-t0)
        self.alignProfilesButton.setEnabled(True)
        self.showSegmentButton.setEnabled(False)
        self.undoAlignButton.setEnabled(False)

    def alignOperation(self, warpedSegments, mainWindow):
        newSignals = list()
        signals = mainWindow.stack[-1].datas
        for i in range(len(signals)):
            if (i != index):
                cow.updateSignal2(signals[i])
                newSignals.append(cow.getAlignedSignals(warpedSegments[i]))
            else:
                newSignals.append(signals[i])

        mainWindow.stack.append(Signals(newSignals))
        mainWindow.plot(index)

        self.undoAlignButton.setEnabled(True)
        self.alignProfilesButton.setEnabled(False)
        self.showSegmentButton.setEnabled(False)

    def undo(self, mainWindow):
        mainWindow.undo()
        self.undoAlignButton.setEnabled(False)
        self.alignProfilesButton.setEnabled(False)
        self.showSegmentButton.setEnabled(True)

    def comboUpdate(self, mainWindow):
        if (len(mainWindow.stack) == 0):
            print("No signal")
        else:
            for i in range(len(mainWindow.stack[-1].datas)):
                self.combo.addItem("Signal-" + str(i + 1))

    def retranslateUi(self, COWParameters):
        _translate = QtCore.QCoreApplication.translate
        COWParameters.setWindowTitle(_translate("COWParameters", "Form"))
        self.COWLabel.setText(_translate("COWParameters", "COW Parameters"))
        self.showSegmentButton.setText(_translate("COWParameters", "Show Segments"))
        self.alignProfilesButton.setText(_translate("COWParameters", "Align Profiles"))
        self.undoAlignButton.setText(_translate("COWParameters", "Undo Alignment"))
        self.refProfileLabel.setText(_translate("COWParameters", "Reference Profile"))
        self.segmentLengthLabel.setText(_translate("COWParameters", "Segment Length"))
        self.segmentLengthLineEdit.setText(_translate("COWParameters", "10"))
        self.slackLabel.setText(_translate("COWParameters", "Slack"))
        self.slackLineEdit.setText(_translate("COWParameters", "3"))


index = None
cow = None

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    COWParameters = QtWidgets.QWidget()
    ui = Ui_COWParameters()
    ui.setupUi(COWParameters)
    COWParameters.show()
    sys.exit(app.exec_())
