
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


class Ui_InputVisualisation(object):

    def setupUi(self, InputVisualisation):
        InputVisualisation.setObjectName("InputVisualisation")
        InputVisualisation.setWindowModality(QtCore.Qt.ApplicationModal)
        InputVisualisation.resize(631, 704)
        self.verticalLayout = QtWidgets.QVBoxLayout(InputVisualisation)
        self.verticalLayout.setContentsMargins(-1, 20, -1, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.input_first = QtWidgets.QFrame(InputVisualisation)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.input_first.sizePolicy().hasHeightForWidth())
        self.input_first.setSizePolicy(sizePolicy)
        self.input_first.setMinimumSize(QtCore.QSize(0, 200))
        self.input_first.setMaximumSize(QtCore.QSize(16777215, 200))
        self.input_first.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.input_first.setFrameShadow(QtWidgets.QFrame.Raised)
        self.input_first.setObjectName("input_first")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.input_first)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.labelInitialStateVecor = QtWidgets.QLabel(self.input_first)
        self.labelInitialStateVecor.setMaximumSize(QtCore.QSize(16777215, 30))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.labelInitialStateVecor.setFont(font)
        self.labelInitialStateVecor.setObjectName("labelInitialStateVecor")
        self.verticalLayout_3.addWidget(self.labelInitialStateVecor)
        self.widget = QtWidgets.QWidget(self.input_first)
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.layoutMatrix_2 = QtWidgets.QVBoxLayout()
        self.layoutMatrix_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.layoutMatrix_2.setObjectName("layoutMatrix_2")
        self.verticalLayout_4.addLayout(self.layoutMatrix_2)
        self.verticalLayout_3.addWidget(self.widget)
        self.verticalLayout.addWidget(self.input_first)
        self.input_second = QtWidgets.QFrame(InputVisualisation)
        self.input_second.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.input_second.setFrameShadow(QtWidgets.QFrame.Raised)
        self.input_second.setObjectName("input_second")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.input_second)
        self.verticalLayout_2.setContentsMargins(-1, 30, -1, -1)
        self.verticalLayout_2.setSpacing(11)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.labelTransitionMatrix = QtWidgets.QLabel(self.input_second)
        self.labelTransitionMatrix.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self.labelTransitionMatrix.setFont(font)
        self.labelTransitionMatrix.setObjectName("labelTransitionMatrix")
        self.verticalLayout_2.addWidget(self.labelTransitionMatrix)
        self.frame = QtWidgets.QFrame(self.input_second)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layoutMatrix = QtWidgets.QVBoxLayout()
        self.layoutMatrix.setObjectName("layoutMatrix")
        self.horizontalLayout.addLayout(self.layoutMatrix)
        self.verticalLayout_2.addWidget(self.frame)
        self.verticalLayout.addWidget(self.input_second)

        self.retranslateUi(InputVisualisation)
        QtCore.QMetaObject.connectSlotsByName(InputVisualisation)

    def retranslateUi(self, InputVisualisation):
        _translate = QtCore.QCoreApplication.translate
        InputVisualisation.setWindowTitle(_translate("InputVisualisation", "Form"))
        self.labelInitialStateVecor.setText(_translate("InputVisualisation", "Initial State Vector:"))
        self.labelTransitionMatrix.setText(_translate("InputVisualisation", "Transition Matrix:"))

