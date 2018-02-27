from PyQt5.QtWidgets import QDialog
from FunSpec4DTMC.view.ErrorDialogs.ui_inputerror import  Ui_InputError

class InputError(QDialog, Ui_InputError):

    def __init__(self):
        """
        Constructor of the class InputError
        """
        super(InputError, self).__init__()
        self.setupUi(self)

