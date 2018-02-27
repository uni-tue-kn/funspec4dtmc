
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


class Ui_displayPrecisionSelectionDialog(object):

    def setupUi(self, displayPrecisionSelectionDialog):
        displayPrecisionSelectionDialog.setObjectName("displayPrecisionSelectionDialog")
        displayPrecisionSelectionDialog.resize(314, 199)
        self.bb_precisitionSelection = QtWidgets.QDialogButtonBox(displayPrecisionSelectionDialog)
        self.bb_precisitionSelection.setGeometry(QtCore.QRect(-70, 140, 341, 32))
        self.bb_precisitionSelection.setOrientation(QtCore.Qt.Horizontal)
        self.bb_precisitionSelection.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.bb_precisitionSelection.setObjectName("bb_precisitionSelection")
        self.la_displayPrecision = QtWidgets.QLabel(displayPrecisionSelectionDialog)
        self.la_displayPrecision.setGeometry(QtCore.QRect(40, 40, 181, 71))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.la_displayPrecision.setFont(font)
        self.la_displayPrecision.setObjectName("la_displayPrecision")
        self.sb_displayPrecision = QtWidgets.QSpinBox(displayPrecisionSelectionDialog)
        self.sb_displayPrecision.setGeometry(QtCore.QRect(220, 60, 51, 31))
        self.sb_displayPrecision.setMinimum(1)
        self.sb_displayPrecision.setProperty("value", 2)
        self.sb_displayPrecision.setObjectName("sb_displayPrecision")

        self.retranslateUi(displayPrecisionSelectionDialog)
        self.bb_precisitionSelection.accepted.connect(displayPrecisionSelectionDialog.accept)
        self.bb_precisitionSelection.rejected.connect(displayPrecisionSelectionDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(displayPrecisionSelectionDialog)

    def retranslateUi(self, displayPrecisionSelectionDialog):
        _translate = QtCore.QCoreApplication.translate
        displayPrecisionSelectionDialog.setWindowTitle(_translate("displayPrecisionSelectionDialog", "Display precision"))
        self.la_displayPrecision.setText(_translate("displayPrecisionSelectionDialog", "Display precision:"))

