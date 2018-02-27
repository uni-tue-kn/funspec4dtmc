# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './inputfileerror.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InputFileError(object):
    def setupUi(self, InputFileError):
        InputFileError.setObjectName("InputFileError")
        InputFileError.resize(431, 196)
        self.bb_err = QtWidgets.QDialogButtonBox(InputFileError)
        self.bb_err.setGeometry(QtCore.QRect(40, 140, 341, 32))
        self.bb_err.setOrientation(QtCore.Qt.Horizontal)
        self.bb_err.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb_err.setObjectName("bb_err")
        self.la_err1 = QtWidgets.QLabel(InputFileError)
        self.la_err1.setGeometry(QtCore.QRect(20, 10, 361, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.la_err1.setFont(font)
        self.la_err1.setStyleSheet("color: rgb(152, 0, 2)")
        self.la_err1.setObjectName("la_err1")
        self.la_err_3 = QtWidgets.QLabel(InputFileError)
        self.la_err_3.setGeometry(QtCore.QRect(20, 80, 361, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.la_err_3.setFont(font)
        self.la_err_3.setStyleSheet("color: rgb(152, 0, 2)")
        self.la_err_3.setObjectName("la_err_3")
        self.la_err_2 = QtWidgets.QLabel(InputFileError)
        self.la_err_2.setGeometry(QtCore.QRect(20, 50, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.la_err_2.setFont(font)
        self.la_err_2.setStyleSheet("color: rgb(152, 0, 2)")
        self.la_err_2.setObjectName("la_err_2")

        self.retranslateUi(InputFileError)
        self.bb_err.accepted.connect(InputFileError.accept)
        self.bb_err.rejected.connect(InputFileError.reject)
        QtCore.QMetaObject.connectSlotsByName(InputFileError)

    def retranslateUi(self, InputFileError):
        _translate = QtCore.QCoreApplication.translate
        InputFileError.setWindowTitle(_translate("InputFileError", "Input Error"))
        self.la_err1.setText(_translate("InputFileError", "Format of the file does not match"))
        self.la_err_3.setText(_translate("InputFileError", "Input is discarded."))
        self.la_err_2.setText(_translate("InputFileError", "the expected input specification."))

