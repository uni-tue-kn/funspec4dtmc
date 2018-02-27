
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

from PyQt5 import QtCore, QtWidgets

class Ui_TransitionFunction(object):

    def setupUi(self, TransitionFunction):
        TransitionFunction.setObjectName("TransitionFunction")
        TransitionFunction.resize(581, 166)
        self.te_tf = QtWidgets.QTextEdit(TransitionFunction)
        self.te_tf.setGeometry(QtCore.QRect(50, 40, 551, 121))
        self.te_tf.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.te_tf.setFrameShadow(QtWidgets.QFrame.Plain)
        self.te_tf.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.te_tf.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.te_tf.setObjectName("te_tf")
        self.stack_tf = QtWidgets.QStackedWidget(TransitionFunction)
        self.stack_tf.setGeometry(QtCore.QRect(10, 20, 601, 21))
        self.stack_tf.setObjectName("stack_tf")
        self.tf0 = QtWidgets.QWidget()
        self.tf0.setObjectName("tf0")
        self.te_tf0_name = QtWidgets.QTextBrowser(self.tf0)
        self.te_tf0_name.setGeometry(QtCore.QRect(0, 0, 591, 21))
        self.te_tf0_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.te_tf0_name.setFrameShadow(QtWidgets.QFrame.Plain)
        self.te_tf0_name.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te_tf0_name.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te_tf0_name.setObjectName("te_tf0_name")
        self.stack_tf.addWidget(self.tf0)
        self.tf1 = QtWidgets.QWidget()
        self.tf1.setObjectName("tf1")
        self.te_tf1_name = QtWidgets.QTextBrowser(self.tf1)
        self.te_tf1_name.setGeometry(QtCore.QRect(0, 0, 591, 21))
        self.te_tf1_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.te_tf1_name.setFrameShadow(QtWidgets.QFrame.Plain)
        self.te_tf1_name.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te_tf1_name.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te_tf1_name.setObjectName("te_tf1_name")
        self.stack_tf.addWidget(self.tf1)
        self.tf2 = QtWidgets.QWidget()
        self.tf2.setObjectName("tf2")
        self.te_tf2_name = QtWidgets.QTextBrowser(self.tf2)
        self.te_tf2_name.setGeometry(QtCore.QRect(0, 0, 591, 21))
        self.te_tf2_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.te_tf2_name.setFrameShadow(QtWidgets.QFrame.Plain)
        self.te_tf2_name.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te_tf2_name.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te_tf2_name.setObjectName("te_tf2_name")
        self.stack_tf.addWidget(self.tf2)
        self.tf3 = QtWidgets.QWidget()
        self.tf3.setObjectName("tf3")
        self.te_tf3_name = QtWidgets.QTextBrowser(self.tf3)
        self.te_tf3_name.setGeometry(QtCore.QRect(0, 0, 521, 21))
        self.te_tf3_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.te_tf3_name.setFrameShadow(QtWidgets.QFrame.Plain)
        self.te_tf3_name.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te_tf3_name.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te_tf3_name.setObjectName("te_tf3_name")
        self.stack_tf.addWidget(self.tf3)
        self.tf4 = QtWidgets.QWidget()
        self.tf4.setObjectName("tf4")
        self.te_tf4_name = QtWidgets.QTextBrowser(self.tf4)
        self.te_tf4_name.setGeometry(QtCore.QRect(0, 0, 591, 21))
        self.te_tf4_name.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.te_tf4_name.setFrameShadow(QtWidgets.QFrame.Plain)
        self.te_tf4_name.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te_tf4_name.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.te_tf4_name.setObjectName("te_tf4_name")
        self.stack_tf.addWidget(self.tf4)
        self.bu_right = QtWidgets.QPushButton(TransitionFunction)
        self.bu_right.setGeometry(QtCore.QRect(30, 6, 21, 21))
        self.bu_right.setAutoFillBackground(False)
        self.bu_right.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.bu_right.setText("")
        self.bu_right.setFlat(True)
        self.bu_right.setObjectName("bu_right")
        self.bu_left = QtWidgets.QPushButton(TransitionFunction)
        self.bu_left.setGeometry(QtCore.QRect(10, 6, 21, 21))
        self.bu_left.setAutoFillBackground(False)
        self.bu_left.setStyleSheet("background-color:rgb(255, 255, 255)")
        self.bu_left.setText("")
        self.bu_left.setFlat(True)
        self.bu_left.setObjectName("bu_left")

        self.retranslateUi(TransitionFunction)
        self.stack_tf.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(TransitionFunction)

    def retranslateUi(self, TransitionFunction):
        _translate = QtCore.QCoreApplication.translate
        TransitionFunction.setWindowTitle(_translate("TransitionFunction", "Dialog"))
        self.te_tf.setHtml(_translate("TransitionFunction", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.te_tf0_name.setHtml(_translate("TransitionFunction", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">def </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function(</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>"))
        self.te_tf1_name.setHtml(_translate("TransitionFunction", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function(float </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, float </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>"))
        self.te_tf2_name.setHtml(_translate("TransitionFunction", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function(tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, float </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>"))
        self.te_tf3_name.setHtml(_translate("TransitionFunction", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function(float </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>"))
        self.te_tf4_name.setHtml(_translate("TransitionFunction", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#cc7832;\">cdef double </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">transition_function(tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">state</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">, tuple </span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#005500;\">factor</span><span style=\" font-family:\'Courier New\'; font-size:9pt; font-weight:600; color:#1e2124;\">):   </span></p></body></html>"))

