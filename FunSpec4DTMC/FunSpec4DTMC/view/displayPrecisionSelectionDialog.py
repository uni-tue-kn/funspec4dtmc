
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

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtWidgets
from FunSpec4DTMC.view.ui_displayprecisionselectiondialog import Ui_displayPrecisionSelectionDialog


class DisplayPrecisionSelectionDialog(QDialog, Ui_displayPrecisionSelectionDialog):
    displayPrecisionAdjusted = pyqtSignal(float, name='displayPrecisionAdjusted')

    def __init__(self):
        """
        Constructor of the class  DisplayPrecisionSelectionDialog
        """
        super(DisplayPrecisionSelectionDialog, self).__init__()
        self.setupUi(self)
        self.precision = 3
        self.bb_precisitionSelection.accepted.connect(self.adjustDisplayPrecision)
        self.bb_precisitionSelection.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.reset)

    def reset(self):
        """
        Function for resetting precision to the initial state with three decimal places
        """
        self.sb_displayPrecision.setValue(self.precision)
        self.adjustDisplayPrecision()

    def adjustDisplayPrecision(self):
        """
        Function for adjusting the display precision
        """
        self.precision = int(self.sb_displayPrecision.value())
        self.displayPrecisionAdjusted.emit(self.precision)
