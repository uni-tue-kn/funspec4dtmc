from PyQt5.QtWidgets import QDialog
from FunSpec4DTMC.view.ErrorDialogs.ui_runtimeWarning import  Ui_runtimeWarning

class RuntimeWarning(QDialog, Ui_runtimeWarning):

    def __init__(self):
        """
        Constructor of the class RuntimeWarning
        """
        super(RuntimeWarning, self).__init__()
        self.setupUi(self)

    def hiding_dialog(self):
        """
        Information about hiding the dialog in future
        :return: whether dialog is hidden
        """
        return self.cb_hideDialog.isChecked()
