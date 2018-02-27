
#  Copyright (C) 2018 University of Tuebingen
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, version 3.
#
#  This program is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_discretizationPrecisionSelectionDialog(object):

    def setupUi(self, discretizationPrecisionSelectionDialog):
        discretizationPrecisionSelectionDialog.setObjectName("discretizationPrecisionSelectionDialog")
        discretizationPrecisionSelectionDialog.resize(383, 200)
        self.bb_precisitionSelection = QtWidgets.QDialogButtonBox(discretizationPrecisionSelectionDialog)
        self.bb_precisitionSelection.setGeometry(QtCore.QRect(20, 140, 341, 32))
        self.bb_precisitionSelection.setOrientation(QtCore.Qt.Horizontal)
        self.bb_precisitionSelection.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb_precisitionSelection.setObjectName("bb_precisitionSelection")
        self.la_discretization_precision = QtWidgets.QLabel(discretizationPrecisionSelectionDialog)
        self.la_discretization_precision.setGeometry(QtCore.QRect(40, 40, 191, 71))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.la_discretization_precision.setFont(font)
        self.la_discretization_precision.setObjectName("la_discretization_precision")
        self.le_discretizationPrecision = QtWidgets.QLineEdit(discretizationPrecisionSelectionDialog)
        self.le_discretizationPrecision.setGeometry(QtCore.QRect(240, 60, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_discretizationPrecision.setFont(font)
        self.le_discretizationPrecision.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.le_discretizationPrecision.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_discretizationPrecision.setObjectName("le_discretizationPrecision")

        self.retranslateUi(discretizationPrecisionSelectionDialog)
        self.bb_precisitionSelection.accepted.connect(discretizationPrecisionSelectionDialog.accept)
        self.bb_precisitionSelection.rejected.connect(discretizationPrecisionSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(discretizationPrecisionSelectionDialog)

    def retranslateUi(self, discretizationPrecisionSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        discretizationPrecisionSelectionDialog.setWindowTitle(_translate("discretizationPrecisionSelectionDialog", "Calculation precision"))
        self.la_discretization_precision.setText(_translate("discretizationPrecisionSelectionDialog", "Discretization precision:"))
        self.le_discretizationPrecision.setText(_translate("discretizationPrecisionSelectionDialog", "10e-9"))

