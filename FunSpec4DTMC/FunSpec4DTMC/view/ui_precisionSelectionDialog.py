
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


class Ui_PrecisionSelectionDialog(object):

    def setupUi(self, PrecisionSelectionDialog):
        PrecisionSelectionDialog.setObjectName("PrecisionSelectionDialog")
        PrecisionSelectionDialog.resize(383, 200)
        self.bb_precisitionSelection = QtWidgets.QDialogButtonBox(PrecisionSelectionDialog)
        self.bb_precisitionSelection.setGeometry(QtCore.QRect(20, 140, 341, 32))
        self.bb_precisitionSelection.setOrientation(QtCore.Qt.Horizontal)
        self.bb_precisitionSelection.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb_precisitionSelection.setObjectName("bb_precisitionSelection")
        self.la_calculation_precision = QtWidgets.QLabel(PrecisionSelectionDialog)
        self.la_calculation_precision.setGeometry(QtCore.QRect(40, 40, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.la_calculation_precision.setFont(font)
        self.la_calculation_precision.setObjectName("la_calculation_precision")
        self.le_calculationPrecision = QtWidgets.QLineEdit(PrecisionSelectionDialog)
        self.le_calculationPrecision.setGeometry(QtCore.QRect(240, 60, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.le_calculationPrecision.setFont(font)
        self.le_calculationPrecision.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.le_calculationPrecision.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.le_calculationPrecision.setObjectName("le_calculationPrecision")

        self.retranslateUi(PrecisionSelectionDialog)
        self.bb_precisitionSelection.accepted.connect(PrecisionSelectionDialog.accept)
        self.bb_precisitionSelection.rejected.connect(PrecisionSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PrecisionSelectionDialog)

    def retranslateUi(self, PrecisionSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        PrecisionSelectionDialog.setWindowTitle(_translate("PrecisionSelectionDialog", "Calculation precision"))
        self.la_calculation_precision.setText(_translate("PrecisionSelectionDialog", "Calculation precision:"))
        self.le_calculationPrecision.setText(_translate("PrecisionSelectionDialog", "10e-16"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PrecisionSelectionDialog = QtWidgets.QDialog()
    ui = Ui_PrecisionSelectionDialog()
    ui.setupUi(PrecisionSelectionDialog)
    PrecisionSelectionDialog.show()
    sys.exit(app.exec_())

