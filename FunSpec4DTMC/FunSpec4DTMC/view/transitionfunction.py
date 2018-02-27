
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
from PyQt5 import QtCore, QtGui
from FunSpec4DTMC.view.ui_transitionfunction import Ui_TransitionFunction



class TransitionFunction(QDialog, Ui_TransitionFunction):

    def __init__(self, index: str=1, fixed=False):
        """
        Constuctor of the class TransitionFunction
        :param index: Index of the transition function
        """
        super(TransitionFunction, self).__init__()
        self.setupUi(self)
        self.stack_tf.setCurrentIndex(0)

        self.bu_left.setIcon(QtGui.QIcon("./resources/icons/leftarrow.png"))
        self.bu_right.setIcon(QtGui.QIcon("./resources/icons/rightarrow.png"))
        self.initialize(index)
        if fixed:
            self.bu_left.setEnabled(False)
            self.bu_left.setVisible(False)
            self.bu_right.setEnabled(False)
            self.bu_right.setVisible(False)

    def initialize(self, index):
        """
        Method to initialize the buttons
        :param index: Index of the transition function
        """
        _translate = QtCore.QCoreApplication.translate
        self.bu_left.clicked.connect(self.reduce_tf_index)
        self.bu_right.clicked.connect(self.increment_tf_index)



        self.te_tf0_name.setHtml(_translate("TransitionFunction",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                            '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">def </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function' + str(
                                                str(index) + '(</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>')))

        self.te_tf1_name.setHtml(_translate("TransitionFunction",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                            '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cpdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function' + str(index) + '(double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>'))

        self.te_tf2_name.setHtml(_translate("TransitionFunction",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                            '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cpdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function' + str(index) + '(tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>'))


        self.te_tf3_name.setHtml(_translate("TransitionFunction",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                            '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cpdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function' + str(index) + '(double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>'))
        self.te_tf4_name.setHtml(_translate("TransitionFunction",
                                            "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                            "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                            "p, li { white-space: pre-wrap; }\n"
                                            "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                            '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cpdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function' + str(index) + '(tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>'))



    def reduce_tf_index(self):
        """
        Method to reduce the current function index
        """
        self.stack_tf.setCurrentIndex((self.stack_tf.currentIndex()-1) % 5)

    def increment_tf_index(self):
        """
        Method to increment the current function index
        """
        self.stack_tf.setCurrentIndex((self.stack_tf.currentIndex()+1) % 5)

    def get_transition_function_name(self):
        """
        Method to get the header of the functions
        :return: function header
        """
        current_index = self.stack_tf.currentIndex()
        if current_index == 0:
            return self.te_tf0_name.toPlainText()
        elif current_index == 1:
            return self.te_tf1_name.toPlainText()
        elif current_index == 2:
            return self.te_tf2_name.toPlainText()
        elif current_index == 3:
            return self.te_tf3_name.toPlainText()
        elif current_index == 4:
            return self.te_tf4_name.toPlainText()
        else:
            raise IndexError

    def get_transition_function(self):
        """
        Method to get the function instructions
        :return: function instructions
        """
        return self.te_tf.toPlainText()

    def set_function(self, function_name, function: str, index):
        """
        Method to set or change the transition function
        :param function: transition function
        """
        index += 1
        function_name = function_name.replace("  ", " ").strip()
        _translate = QtCore.QCoreApplication.translate

        try:
            import cython
        except:
            self.cython_mode=False

        if function_name.strip() != "":
            if "(state, factor)" in function_name or not self.cython_mode:
                self.te_tf0_name.setHtml(_translate("TransitionFunction",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                    '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">def </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function' +str(index) + '(</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>'))
            elif "(double state, double factor)" in function_name:
                self.stack_tf.setCurrentIndex(1)
                self.te_tf1_name.setHtml(_translate("TransitionFunction",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                    '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cpdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function'+ str(index)+'(double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>'))
            elif "(tuple state, double factor)" in function_name:
                self.stack_tf.setCurrentIndex(2)
                self.te_tf2_name.setHtml(_translate("TransitionFunction",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                    '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cpdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function'+str(index)+'(tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>'))

            elif "(double state, tuple factor)" in function_name:
                self.stack_tf.setCurrentIndex(3)
                self.te_tf3_name.setHtml(_translate("TransitionFunction",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                    '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cpdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function'+str(index)+'(double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>'))

            elif "(tuple state, tuple factor)"in function_name:
                self.stack_tf.setCurrentIndex(4)
                self.te_tf4_name.setHtml(_translate("TransitionFunction",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
                                                    '<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cpdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function'+ str(index) +'(tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>'))

            else:
                raise IndexError

        function_lines = ""
        for index in range(0, len(function)):
            if function != "":
                if type(function) is list:
                    function_lines += function[index].strip()
                    function_lines += "\n"
                else:
                    function_lines += function[index]
        while "\n " in function_lines:
            function_lines = function_lines.replace("\n ", "\n")
        function_lines = function_lines.strip()
        self.te_tf.setText(function_lines)
