# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './runtimeWarning.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_runtimeWarning(object):
    def setupUi(self, runtimeWarning):
        runtimeWarning.setObjectName("runtimeWarning")
        runtimeWarning.resize(528, 287)
        self.bb_err = QtWidgets.QDialogButtonBox(runtimeWarning)
        self.bb_err.setGeometry(QtCore.QRect(80, 230, 431, 32))
        self.bb_err.setOrientation(QtCore.Qt.Horizontal)
        self.bb_err.setStandardButtons(QtWidgets.QDialogButtonBox.No|QtWidgets.QDialogButtonBox.Yes)
        self.bb_err.setObjectName("bb_err")
        self.la_err1 = QtWidgets.QLabel(runtimeWarning)
        self.la_err1.setGeometry(QtCore.QRect(20, 20, 461, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.la_err1.setFont(font)
        self.la_err1.setStyleSheet("color: rgb(152, 0, 2)")
        self.la_err1.setObjectName("la_err1")
        self.la_err2 = QtWidgets.QLabel(runtimeWarning)
        self.la_err2.setGeometry(QtCore.QRect(20, 70, 461, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.la_err2.setFont(font)
        self.la_err2.setStyleSheet("color: rgb(152, 0, 2)")
        self.la_err2.setObjectName("la_err2")
        self.la_err3 = QtWidgets.QLabel(runtimeWarning)
        self.la_err3.setGeometry(QtCore.QRect(20, 120, 501, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.la_err3.setFont(font)
        self.la_err3.setStyleSheet("color: rgb(152, 0, 2)")
        self.la_err3.setObjectName("la_err3")
        self.cb_hideDialog = QtWidgets.QCheckBox(runtimeWarning)
        self.cb_hideDialog.setGeometry(QtCore.QRect(30, 180, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.cb_hideDialog.setFont(font)
        self.cb_hideDialog.setObjectName("cb_hideDialog")

        self.retranslateUi(runtimeWarning)
        self.bb_err.accepted.connect(runtimeWarning.accept)
        self.bb_err.rejected.connect(runtimeWarning.reject)
        QtCore.QMetaObject.connectSlotsByName(runtimeWarning)

    def retranslateUi(self, runtimeWarning):
        _translate = QtCore.QCoreApplication.translate
        runtimeWarning.setWindowTitle(_translate("runtimeWarning", "Calculation Error"))
        self.la_err1.setText(_translate("runtimeWarning", "Input visualization takes longer than expected."))
        self.la_err2.setText(_translate("runtimeWarning", "Do you want to continue calculation?"))
        self.la_err3.setText(_translate("runtimeWarning", "The calculation of the input visualization continues."))
        self.cb_hideDialog.setText(_translate("runtimeWarning", "Do not display the dialog again,"))

