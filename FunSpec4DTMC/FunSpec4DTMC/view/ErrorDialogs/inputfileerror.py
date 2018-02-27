from PyQt5.QtWidgets import QDialog
from FunSpec4DTMC.view.ErrorDialogs.ui_inputfileerror import  Ui_InputFileError

class InputFileError(QDialog, Ui_InputFileError):

    def __init__(self):
        """
        Constructor of the class InputFileError
        """
        super(InputFileError, self).__init__()
        self.setupUi(self)

