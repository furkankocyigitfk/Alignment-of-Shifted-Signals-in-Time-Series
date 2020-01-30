# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DTWParameters.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!
from DTWFunctions import DTWFunctions
from IBAligner import IBAligner
from SCBAligner import SCBAligner
from Signal import Signals
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DTWParameters(object):
    def setupUi(self, DTWParameters, mainWindow):
        signals = mainWindow.stack[-1].datas
        if len(signals) <= 2:
            mainWindow.actionShow_Signals_On_Seperate_Axes.setChecked(False)
        else:
            mainWindow.actionShow_Signals_On_Seperate_Axes.setChecked(True)

        global index
        global dtw
        index = None
        dtw = None
        DTWParameters.setObjectName("DTWParameters")
        DTWParameters.resize(440, 400)
        DTWParameters.setMaximumSize(QtCore.QSize(440, 400))
        self.PTWParametereLabel = QtWidgets.QLabel(DTWParameters)
        self.PTWParametereLabel.setGeometry(QtCore.QRect(85, 10, 230, 30))
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PTWParametereLabel.setFont(font)
        self.PTWParametereLabel.setObjectName("PTWParametereLabel")
        self.layoutWidget = QtWidgets.QWidget(DTWParameters)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 350, 356, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.alignProfilesButton = QtWidgets.QPushButton(self.layoutWidget)
        self.alignProfilesButton.setEnabled(False)
        self.alignProfilesButton.setObjectName("alignProfilesButton")
        self.horizontalLayout_4.addWidget(self.alignProfilesButton)
        self.undoAlignButton = QtWidgets.QPushButton(self.layoutWidget)
        self.undoAlignButton.setEnabled(False)
        self.undoAlignButton.setObjectName("undoAlignButton")
        self.horizontalLayout_4.addWidget(self.undoAlignButton)
        self.showPathButton = QtWidgets.QPushButton(self.layoutWidget)
        self.showPathButton.setObjectName("showPathButton")
        self.horizontalLayout_4.addWidget(self.showPathButton)
        self.layoutWidget1 = QtWidgets.QWidget(DTWParameters)
        self.layoutWidget1.setGeometry(QtCore.QRect(240, 250, 141, 47))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.refProfileLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.refProfileLabel.setObjectName("refProfileLabel")
        self.verticalLayout_2.addWidget(self.refProfileLabel)
        self.comboBox_2 = QtWidgets.QComboBox(self.layoutWidget1)
        self.comboBox_2.setObjectName("comboBox_2")
        self.combo2Update(mainWindow)
        self.verticalLayout_2.addWidget(self.comboBox_2)
        self.layoutWidget2 = QtWidgets.QWidget(DTWParameters)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 250, 151, 47))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.distMethodLabel = QtWidgets.QLabel(self.layoutWidget2)
        self.distMethodLabel.setObjectName("distMethodLabel")
        self.verticalLayout.addWidget(self.distMethodLabel)
        self.comboBox = QtWidgets.QComboBox(self.layoutWidget2)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.layoutWidget3 = QtWidgets.QWidget(DTWParameters)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 60, 151, 171))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.additionalLabel = QtWidgets.QLabel(self.layoutWidget3)
        self.additionalLabel.setObjectName("additionalLabel")
        self.verticalLayout_4.addWidget(self.additionalLabel)
        self.derivativeCheckBox = QtWidgets.QCheckBox(self.layoutWidget3)
        self.derivativeCheckBox.setObjectName("derivativeCheckBox")
        self.verticalLayout_4.addWidget(self.derivativeCheckBox)
        self.timePenaltyCheckBox = QtWidgets.QCheckBox(self.layoutWidget3)
        self.timePenaltyCheckBox.setObjectName("timePenaltyCheckBox")
        self.timePenaltyCheckBox.clicked.connect(
            lambda: self.timeValueLineEdit.setEnabled(self.timePenaltyCheckBox.isChecked()))
        self.verticalLayout_4.addWidget(self.timePenaltyCheckBox)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.timeValueLabel = QtWidgets.QLabel(self.layoutWidget3)
        self.timeValueLabel.setObjectName("timeValueLabel")
        self.horizontalLayout.addWidget(self.timeValueLabel)
        self.timeValueLineEdit = QtWidgets.QLineEdit(self.layoutWidget3)
        self.timeValueLineEdit.setEnabled(False)
        self.timeValueLineEdit.setMaximumSize(QtCore.QSize(40, 20))
        self.timeValueLineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.timeValueLineEdit.setObjectName("timeValueLineEdit")
        self.horizontalLayout.addWidget(self.timeValueLineEdit)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.gapPenaltyCheckBox = QtWidgets.QCheckBox(self.layoutWidget3)
        self.gapPenaltyCheckBox.setObjectName("gapPenaltyCheckBox")
        self.gapPenaltyCheckBox.clicked.connect(
            lambda: self.gapPenaltyLineEdit.setEnabled(self.gapPenaltyCheckBox.isChecked()))
        self.verticalLayout_4.addWidget(self.gapPenaltyCheckBox)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gapValueLabel = QtWidgets.QLabel(self.layoutWidget3)
        self.gapValueLabel.setObjectName("gapValueLabel")
        self.horizontalLayout_2.addWidget(self.gapValueLabel)
        self.gapPenaltyLineEdit = QtWidgets.QLineEdit(self.layoutWidget3)
        self.gapPenaltyLineEdit.setMaximumSize(QtCore.QSize(40, 20))
        self.gapPenaltyLineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.gapPenaltyLineEdit.setObjectName("gapPenaltyLineEdit")
        self.gapPenaltyLineEdit.setEnabled(False)
        self.horizontalLayout_2.addWidget(self.gapPenaltyLineEdit)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.widget = QtWidgets.QWidget(DTWParameters)
        self.widget.setGeometry(QtCore.QRect(240, 170, 141, 22))
        self.widget.setObjectName("widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.bandWidthLabel = QtWidgets.QLabel(self.widget)
        self.bandWidthLabel.setObjectName("bandWidthLabel")
        self.horizontalLayout_3.addWidget(self.bandWidthLabel)
        self.bandWidthLineEdit = QtWidgets.QLineEdit(self.widget)
        self.bandWidthLineEdit.setEnabled(False)
        self.bandWidthLineEdit.setMaximumSize(QtCore.QSize(40, 20))
        self.bandWidthLineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.bandWidthLineEdit.setObjectName("bandWidthLineEdit")
        self.horizontalLayout_3.addWidget(self.bandWidthLineEdit)
        self.widget1 = QtWidgets.QWidget(DTWParameters)
        self.widget1.setGeometry(QtCore.QRect(240, 60, 151, 47))
        self.widget1.setObjectName("widget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.opTechLabel = QtWidgets.QLabel(self.widget1)
        self.opTechLabel.setObjectName("opTechLabel")
        self.verticalLayout_3.addWidget(self.opTechLabel)
        self.comboBox_3 = QtWidgets.QComboBox(self.widget1)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.activated.connect(self.combo3Op)
        self.verticalLayout_3.addWidget(self.comboBox_3)

        isDerivative = self.derivativeCheckBox.isChecked()
        if isDerivative:
            for signal in signals:
                self.derivate(signal)

        warping_paths = [None] * (len(signals))

        self.showPathButton.clicked.connect(lambda: self.showWarpingPaths(warping_paths, mainWindow))
        self.alignProfilesButton.clicked.connect(lambda: self.alignOperation(warping_paths, mainWindow))
        self.undoAlignButton.clicked.connect(lambda: self.undo(mainWindow))
        self.retranslateUi(DTWParameters)
        QtCore.QMetaObject.connectSlotsByName(DTWParameters)

    def showWarpingPaths(self, warping_paths, mainWindow):
        global index
        global dtw
        optimizationMethod = self.comboBox_3.currentIndex()
        index = self.comboBox_2.currentIndex()  # signal
        timePenalty = 0.0
        gapPenalty = 3
        bandWidth = 0.0
        distanceMethods = self.comboBox.currentIndex()
        signals = mainWindow.stack[-1].datas
        if self.timePenaltyCheckBox.isChecked():
            timePenalty = float(self.timeValueLineEdit.text())
        if self.gapPenaltyCheckBox.isChecked():
            gapPenalty = int(self.gapPenaltyLineEdit.text())
        if self.bandWidthLineEdit.isEnabled():
            bandWidth = float(self.bandWidthLineEdit.text())
            if (bandWidth <= 0 or bandWidth >= 1):
                print("Please, enter a real number between 0 and 1 as bandwidth parameter.")
                return

        if (optimizationMethod == 0):
            dtw = DTWFunctions(signals[index], gapPenalty, distanceMethods, timePenalty)
        elif (optimizationMethod == 1):
            dtw = IBAligner(signals[index], gapPenalty, bandWidth, distanceMethods, timePenalty)
        else:
            dtw = SCBAligner(signals[index], gapPenalty, bandWidth, distanceMethods, timePenalty)

        lines = list()
        for i in range(len(signals)):
            if i != index:
                dtw.updateSignal2(signals[i])
                warping_paths[i] = dtw.getWarpedPath()
                lines.append(dtw.forPlotWarpedSegments(warping_paths[i]))
            else:
                lines.append(None)

        mainWindow.plotWarpedSegment(index, lines)
        self.alignProfilesButton.setEnabled(True)
        self.showPathButton.setEnabled(False)
        self.undoAlignButton.setEnabled(False)

    def alignOperation(self, warping_paths, mainWindow):
        newSignals = list()
        signals = mainWindow.stack[-1].datas
        for i in range(len(signals)):
            if (i != index):
                dtw.updateSignal2(signals[i])
                newSignals.append(dtw.getAlignedSignal(warping_paths[i]))
            else:
                newSignals.append(signals[i])

        mainWindow.stack.append(Signals(newSignals))
        mainWindow.plot(index)

        self.undoAlignButton.setEnabled(True)
        self.alignProfilesButton.setEnabled(False)
        self.showPathButton.setEnabled(False)

    def undo(self, mainWindow):
        mainWindow.undo()
        self.undoAlignButton.setEnabled(False)
        self.alignProfilesButton.setEnabled(False)
        self.showPathButton.setEnabled(True)

    def derivate(self, signal):
        for i in range(len(signal)):
            signal[i] -= signal[i - 1]

        signal[0] = signal[1]

    def combo3Op(self):
        if self.comboBox_3.currentIndex() != 0:
            self.bandWidthLineEdit.setEnabled(True)
        else:
            self.bandWidthLineEdit.setEnabled(False)

    def combo2Update(self, mainWindow):
        if (len(mainWindow.stack) == 0):
            print("No signal")
        else:
            for i in range(len(mainWindow.stack[-1].datas)):
                self.comboBox_2.addItem("Signal-" + str(i + 1))

    def retranslateUi(self, DTWParameters):
        _translate = QtCore.QCoreApplication.translate
        DTWParameters.setWindowTitle(_translate("DTWParameters", "Form"))
        self.PTWParametereLabel.setText(_translate("DTWParameters", "DTW Parameters"))
        self.alignProfilesButton.setText(_translate("DTWParameters", "Align Profiles"))
        self.undoAlignButton.setText(_translate("DTWParameters", "Undo Alignment"))
        self.showPathButton.setText(_translate("DTWParameters", "Show Warping Path"))
        self.refProfileLabel.setText(_translate("DTWParameters", "Reference Profile"))
        self.distMethodLabel.setText(_translate("DTWParameters", "Distance Methods"))
        self.comboBox.setItemText(0, _translate("DTWParameters", "Euclidean"))
        self.comboBox.setItemText(1, _translate("DTWParameters", "Chessboard"))
        self.comboBox.setItemText(2, _translate("DTWParameters", "Manhattan"))
        self.comboBox.setItemText(3, _translate("DTWParameters", "Bray-Curtis"))
        self.additionalLabel.setText(_translate("DTWParameters", "Additional"))
        self.derivativeCheckBox.setText(_translate("DTWParameters", "is Derivative?"))
        self.timePenaltyCheckBox.setText(_translate("DTWParameters", "Time Penalty"))
        self.timeValueLabel.setText(_translate("DTWParameters", "Time Value"))
        self.timeValueLineEdit.setText(_translate("DTWParameters", "0.05"))
        self.gapPenaltyCheckBox.setText(_translate("DTWParameters", "Gap Penalty"))
        self.gapValueLabel.setText(_translate("DTWParameters", "Gap Value"))
        self.gapPenaltyLineEdit.setText(_translate("DTWParameters", "3"))
        self.bandWidthLabel.setText(_translate("DTWParameters", "Band Width"))
        self.bandWidthLineEdit.setText(_translate("DTWParameters", "0.5"))
        self.opTechLabel.setText(_translate("DTWParameters", "Optimization Technique"))
        self.comboBox_3.setItemText(0, _translate("DTWParameters", "Classic"))
        self.comboBox_3.setItemText(1, _translate("DTWParameters", "Itakura Band"))
        self.comboBox_3.setItemText(2, _translate("DTWParameters", "Sakoe Chiba Band"))


index = None
dtw = None
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    DTWParameters = QtWidgets.QWidget()
    ui = Ui_DTWParameters()
    ui.setupUi(DTWParameters)
    DTWParameters.show()
    sys.exit(app.exec_())
