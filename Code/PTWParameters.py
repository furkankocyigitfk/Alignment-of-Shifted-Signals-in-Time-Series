# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PTWParameters1.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PTWFunctions import PTWFunctions
from Signal import Signals


class Ui_PTWParameters(object):
    def setupUi(self, PTWParameters, mainWindow):
        signals = mainWindow.stack[-1].datas
        if len(signals) <= 2:
            mainWindow.actionShow_Signals_On_Seperate_Axes.setChecked(False)
        else:
            mainWindow.actionShow_Signals_On_Seperate_Axes.setChecked(True)

        PTWParameters.setObjectName("PTWParameters")
        PTWParameters.resize(300, 350)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PTWParameters.sizePolicy().hasHeightForWidth())
        PTWParameters.setSizePolicy(sizePolicy)
        self.PTWParametersLabel = QtWidgets.QLabel(PTWParameters)
        self.PTWParametersLabel.setGeometry(QtCore.QRect(35, 11, 230, 33))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PTWParametersLabel.sizePolicy().hasHeightForWidth())
        self.PTWParametersLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.PTWParametersLabel.setFont(font)
        self.PTWParametersLabel.setObjectName("PTWParametersLabel")
        self.widget = QtWidgets.QWidget(PTWParameters)
        self.widget.setGeometry(QtCore.QRect(10, 70, 121, 47))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.refProfileLabel = QtWidgets.QLabel(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refProfileLabel.sizePolicy().hasHeightForWidth())
        self.refProfileLabel.setSizePolicy(sizePolicy)
        self.refProfileLabel.setObjectName("refProfileLabel")
        self.verticalLayout.addWidget(self.refProfileLabel)
        self.combo = QtWidgets.QComboBox(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.combo.sizePolicy().hasHeightForWidth())
        self.combo.setSizePolicy(sizePolicy)
        self.combo.setObjectName("combo")
        self.verticalLayout.addWidget(self.combo)
        self.widget1 = QtWidgets.QWidget(PTWParameters)
        self.widget1.setGeometry(QtCore.QRect(170, 70, 102, 171))
        self.widget1.setObjectName("widget1")
        self.gridLayout = QtWidgets.QGridLayout(self.widget1)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.warpingFuncLabel = QtWidgets.QLabel(self.widget1)
        font = QtGui.QFont()
        font.setFamily("Tahoma")
        font.setPointSize(8)
        self.warpingFuncLabel.setFont(font)
        self.warpingFuncLabel.setObjectName("warpingFuncLabel")
        self.gridLayout.addWidget(self.warpingFuncLabel, 0, 0, 1, 1)
        self.x2Label = QtWidgets.QLabel(self.widget1)
        self.x2Label.setObjectName("x2Label")
        self.gridLayout.addWidget(self.x2Label, 1, 0, 1, 1)
        self.x2LineEdit = QtWidgets.QLineEdit(self.widget1)
        self.x2LineEdit.setMaximumSize(QtCore.QSize(40, 20))
        self.x2LineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.x2LineEdit.setObjectName("x2LineEdit")
        self.gridLayout.addWidget(self.x2LineEdit, 2, 0, 1, 1)
        self.x1Label = QtWidgets.QLabel(self.widget1)
        self.x1Label.setObjectName("x1Label")
        self.gridLayout.addWidget(self.x1Label, 3, 0, 1, 1)
        self.x1LineEdit = QtWidgets.QLineEdit(self.widget1)
        self.x1LineEdit.setMaximumSize(QtCore.QSize(40, 20))
        self.x1LineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.x1LineEdit.setObjectName("x1LineEdit")
        self.gridLayout.addWidget(self.x1LineEdit, 4, 0, 1, 1)
        self.x0Label = QtWidgets.QLabel(self.widget1)
        self.x0Label.setObjectName("x0Label")
        self.gridLayout.addWidget(self.x0Label, 5, 0, 1, 1)
        self.x0LineEdit = QtWidgets.QLineEdit(self.widget1)
        self.x0LineEdit.setMaximumSize(QtCore.QSize(40, 20))
        self.x0LineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.x0LineEdit.setObjectName("x0LineEdit")
        self.gridLayout.addWidget(self.x0LineEdit, 6, 0, 1, 1)
        self.widget2 = QtWidgets.QWidget(PTWParameters)
        self.widget2.setGeometry(QtCore.QRect(10, 170, 124, 71))
        self.widget2.setObjectName("widget2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.smoothSignalCheckBox = QtWidgets.QCheckBox(self.widget2)
        self.smoothSignalCheckBox.setObjectName("smoothSignalCheckBox")
        self.gridLayout_2.addWidget(self.smoothSignalCheckBox, 0, 0, 1, 2)
        self.gapPenaltyCheckBox = QtWidgets.QCheckBox(self.widget2)
        self.gapPenaltyCheckBox.setObjectName("gapPenaltyCheckBox")
        self.gapPenaltyCheckBox.clicked.connect(
            lambda: self.gapPenaltyLineEdit.setEnabled(self.gapPenaltyCheckBox.isChecked()))
        self.gridLayout_2.addWidget(self.gapPenaltyCheckBox, 1, 0, 1, 2)
        self.gapValueLabel = QtWidgets.QLabel(self.widget2)
        self.gapValueLabel.setObjectName("gapValueLabel")
        self.gridLayout_2.addWidget(self.gapValueLabel, 2, 0, 1, 1)
        self.gapPenaltyLineEdit = QtWidgets.QLineEdit(self.widget2)
        self.gapPenaltyLineEdit.setEnabled(False)
        self.gapPenaltyLineEdit.setMaximumSize(QtCore.QSize(40, 20))
        self.gapPenaltyLineEdit.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.gapPenaltyLineEdit.setObjectName("gapPenaltyLineEdit")
        self.gridLayout_2.addWidget(self.gapPenaltyLineEdit, 2, 1, 1, 1)
        self.splitter = QtWidgets.QSplitter(PTWParameters)
        self.splitter.setGeometry(QtCore.QRect(10, 300, 271, 28))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.alignProfileButton = QtWidgets.QPushButton(self.splitter)
        self.alignProfileButton.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.alignProfileButton.sizePolicy().hasHeightForWidth())
        self.alignProfileButton.setSizePolicy(sizePolicy)
        self.alignProfileButton.setObjectName("alignProfileButton")
        self.undoAlignButton = QtWidgets.QPushButton(self.splitter)
        self.undoAlignButton.setEnabled(False)
        self.undoAlignButton.setObjectName("undoAlignButton")
        self.retranslateUi(PTWParameters)
        QtCore.QMetaObject.connectSlotsByName(PTWParameters)

        self.comboUpdate(mainWindow)
        self.alignProfileButton.clicked.connect(lambda: self.PTWOperation(mainWindow))
        self.undoAlignButton.clicked.connect(lambda: self.undo(mainWindow))

    def undo(self, mainWindow):
        mainWindow.undo()
        self.undoAlignButton.setEnabled(False)
        self.alignProfileButton.setEnabled(True)

    def PTWOperation(self, mainWindow):
        x2 = int(self.x2LineEdit.text())  # str
        x1 = int(self.x1LineEdit.text())
        x0 = int(self.x0LineEdit.text())
        gap = 1
        if (self.gapPenaltyCheckBox.isChecked()):
            gap = int(self.gapPenaltyLineEdit.text())
        IsSmooth = self.smoothSignalCheckBox.isChecked()
        warpFunction = [x2, x1, x0]
        index = self.combo.currentIndex()
        signals = mainWindow.stack[-1].datas
        ptw = PTWFunctions(signals[index], IsSmooth, 1e-5, gap, warpFunction)
        newSignals = list()
        for i in range(len(signals)):
            if (i != index):
                ptw.updateSignal2(signals[i])
                newSignals.append(ptw.getWarpedSignals())
            else:
                newSignals.append(signals[index])
        mainWindow.stack.append(Signals(newSignals))
        mainWindow.plot(index)
        self.alignProfileButton.setEnabled(False)
        self.undoAlignButton.setEnabled(True)

    def comboUpdate(self, mainWindow):
        if (len(mainWindow.stack) == 0):
            print("No signal")
        else:
            for i in range(len(mainWindow.stack[-1].datas)):
                self.combo.addItem("Signal-" + str(i + 1))

    def retranslateUi(self, PTWParameters):
        _translate = QtCore.QCoreApplication.translate
        PTWParameters.setWindowTitle(_translate("PTWParameters", "Form"))
        self.PTWParametersLabel.setText(_translate("PTWParameters", "PTW Parameters"))
        self.refProfileLabel.setText(_translate("PTWParameters", "Reference Profile"))
        self.warpingFuncLabel.setText(_translate("PTWParameters", "Warping Function"))
        self.x2Label.setText(_translate("PTWParameters", "X^2"))
        self.x2LineEdit.setText(_translate("PTWParameters", "0"))
        self.x1Label.setText(_translate("PTWParameters", "X^1"))
        self.x1LineEdit.setText(_translate("PTWParameters", "1"))
        self.x0Label.setText(_translate("PTWParameters", "X^0"))
        self.x0LineEdit.setText(_translate("PTWParameters", "0"))
        self.smoothSignalCheckBox.setText(_translate("PTWParameters", "Smooth Signals?"))
        self.gapPenaltyCheckBox.setText(_translate("PTWParameters", "Gap Penalty"))
        self.gapValueLabel.setText(_translate("PTWParameters", "Gap Value"))
        self.gapPenaltyLineEdit.setText(_translate("PTWParameters", "3"))
        self.alignProfileButton.setText(_translate("PTWParameters", "Align Profiles"))
        self.undoAlignButton.setText(_translate("PTWParameters", "Undo Alignment"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    PTWParameters = QtWidgets.QWidget()
    ui = Ui_PTWParameters()
    ui.setupUi(PTWParameters)
    PTWParameters.show()
    sys.exit(app.exec_())
