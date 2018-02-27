# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './inputerror.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_InputError(object):
    def setupUi(self, InputError):
        InputError.setObjectName("InputError")
        InputError.resize(431, 196)
        self.bb_err = QtWidgets.QDialogButtonBox(InputError)
        self.bb_err.setGeometry(QtCore.QRect(40, 140, 341, 32))
        self.bb_err.setOrientation(QtCore.Qt.Horizontal)
        self.bb_err.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb_err.setObjectName("bb_err")
        self.la_err1 = QtWidgets.QLabel(InputError)
        self.la_err1.setGeometry(QtCore.QRect(20, 10, 361, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.la_err1.setFont(font)
        self.la_err1.setStyleSheet("color: rgb(152, 0, 2)")
        self.la_err1.setObjectName("la_err1")
        self.la_err_3 = QtWidgets.QLabel(InputError)
        self.la_err_3.setGeometry(QtCore.QRect(20, 80, 361, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.la_err_3.setFont(font)
        self.la_err_3.setStyleSheet("color: rgb(152, 0, 2)")
        self.la_err_3.setObjectName("la_err_3")
        self.la_err_2 = QtWidgets.QLabel(InputError)
        self.la_err_2.setGeometry(QtCore.QRect(20, 50, 361, 41))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.la_err_2.setFont(font)
        self.la_err_2.setStyleSheet("color: rgb(152, 0, 2)")
        self.la_err_2.setObjectName("la_err_2")

        self.retranslateUi(InputError)
        self.bb_err.accepted.connect(InputError.accept)
        self.bb_err.rejected.connect(InputError.reject)
        QtCore.QMetaObject.connectSlotsByName(InputError)

    def retranslateUi(self, InputError):
        _translate = QtCore.QCoreApplication.translate
        InputError.setWindowTitle(_translate("InputError", "Input Error"))
        self.la_err1.setText(_translate("InputError", "Format of the file does not match"))
        self.la_err_3.setText(_translate("InputError", "Input is discarded."))
        self.la_err_2.setText(_translate("InputError", "the expected input specification."))

