# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './calculationerror.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CalculationError(object):
    def setupUi(self, CalculationError):
        CalculationError.setObjectName("CalculationError")
        CalculationError.resize(388, 223)
        self.bb_err = QtWidgets.QDialogButtonBox(CalculationError)
        self.bb_err.setGeometry(QtCore.QRect(30, 160, 341, 32))
        self.bb_err.setOrientation(QtCore.Qt.Horizontal)
        self.bb_err.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb_err.setObjectName("bb_err")
        self.la_err1 = QtWidgets.QLabel(CalculationError)
        self.la_err1.setGeometry(QtCore.QRect(20, -30, 361, 171))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.la_err1.setFont(font)
        self.la_err1.setStyleSheet("color: rgb(152, 0, 2)")
        self.la_err1.setObjectName("la_err1")
        self.la_err2 = QtWidgets.QLabel(CalculationError)
        self.la_err2.setGeometry(QtCore.QRect(20, 80, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.la_err2.setFont(font)
        self.la_err2.setStyleSheet("color: rgb(152, 0, 2)")
        self.la_err2.setObjectName("la_err2")

        self.retranslateUi(CalculationError)
        self.bb_err.accepted.connect(CalculationError.accept)
        self.bb_err.rejected.connect(CalculationError.reject)
        QtCore.QMetaObject.connectSlotsByName(CalculationError)

    def retranslateUi(self, CalculationError):
        _translate = QtCore.QCoreApplication.translate
        CalculationError.setWindowTitle(_translate("CalculationError", "Calculation Error"))
        self.la_err1.setText(_translate("CalculationError", "The calculation was interrupted or"))
        self.la_err2.setText(_translate("CalculationError", "a runtime error occurred."))

