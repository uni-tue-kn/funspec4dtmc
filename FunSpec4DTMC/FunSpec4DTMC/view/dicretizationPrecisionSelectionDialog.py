
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

from PyQt5.QtWidgets import QWidget, QDialog
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtWidgets
from FunSpec4DTMC.view.ui_discreticationPrecisionSelectionDialog import Ui_discretizationPrecisionSelectionDialog


class DiscretizationPrecisionSelectionDialog(QDialog, Ui_discretizationPrecisionSelectionDialog):
    discretizationPrecisionAdjusted = pyqtSignal(float, name='discretizationPrecisionAdjusted')

    def __init__(self):
        """
        Constructor of the class  DisplayPrecisionSelectionDialog
        """
        super(DiscretizationPrecisionSelectionDialog, self).__init__()
        self.setupUi(self)
        self.precision = 10e-9
        self.bb_precisitionSelection.accepted.connect(self.adjust_discretization_precision)
        self.bb_precisitionSelection.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reset)

    def reset(self):
        """
        Function for resetting disretization precision
        """
        self.le_discretizationPrecision.setText("10e-9")
        self.adjust_discretization_precision()

    def adjust_discretization_precision(self):
        """
        Function for adjusting the discretization precision
        """
        self.discretizationPrecisionAdjusted.emit(float(self.le_discretizationPrecision.text()))