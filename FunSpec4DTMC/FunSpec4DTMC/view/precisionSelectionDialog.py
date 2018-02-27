
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

from FunSpec4DTMC.view.ui_precisionSelectionDialog import Ui_PrecisionSelectionDialog
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets


class PrecisionSelectionDialog(QDialog, Ui_PrecisionSelectionDialog):
    calculationPrecisionAdjusted = pyqtSignal(float, name='calculationPrecisionAdjusted')

    def __init__(self):
        """
        Constructor of the class PrecisionSelectionDialog
        """
        super(PrecisionSelectionDialog, self).__init__()
        self.setupUi(self)
        self.precision = float("10e-16")
        self.bb_precisitionSelection.accepted.connect(self.adjustCalculationPrecision)
        self.bb_precisitionSelection.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reset)

    def reset(self):
        """
        Method to reset the calculation precision to 10^-16
        """
        self.le_calculationPrecision.setText(str(self.precision))

    def adjustCalculationPrecision(self):
        """
        Method to adjust the calculation precision of the simulator
        """
        self.precision = float(self.le_calculationPrecision.text())
        self.calculationPrecisionAdjusted.emit(self.precision)
