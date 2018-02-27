
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

from PyQt5.QtWidgets import QScrollArea
from PyQt5 import QtWidgets
from FunSpec4DTMC.view.ui_functionalinput import  Ui_FunctionalInput
from FunSpec4DTMC.view.transitionfunction import TransitionFunction


class FunctionalInput(QScrollArea, Ui_FunctionalInput):

    def __init__(self):
        """
        Constructor of the class Functionalnput
        """
        super(FunctionalInput, self).__init__()
        self.setupUi(self)

    def add_transition_function(self, functions):
        """
        Mthod to generate the tabs for displaying the transition functions
        :param functions: transition function input
        """

        layout_tf = QtWidgets.QVBoxLayout()
        for index in range(len(functions)):
            transition_function_name = (functions[index]).splitlines()[0]
            transition_function = "\n".join(functions[index].splitlines()[1:])
            tf = TransitionFunction(str(index), True)
            tf.set_function(transition_function_name, transition_function, index)
            layout_tf.addWidget(tf)

        self.wid_transitionFunction.setLayout(layout_tf)

