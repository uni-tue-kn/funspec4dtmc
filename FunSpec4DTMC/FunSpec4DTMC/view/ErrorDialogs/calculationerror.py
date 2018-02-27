from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from FunSpec4DTMC.view.ErrorDialogs.ui_calculationerror import  Ui_CalculationError

class CalculationError(QDialog, Ui_CalculationError):

    def __init__(self):
        """
        Constructor of the class CalculatioError
        """
        super(CalculationError, self).__init__()
        self.setupUi(self)

