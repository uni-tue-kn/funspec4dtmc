
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

from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QFileDialog
import numpy as np
from FunSpec4DTMC.view.systemSpecificationDialog import SystemSpecificationDialog
from FunSpec4DTMC.view.transitionfunction import TransitionFunction
from FunSpec4DTMC.view.ui_inputdialog import Ui_InputDialog


class InputDialog(QDialog, Ui_InputDialog):
    mcInputConfirmed = pyqtSignal(str, dict, bool, name='mcInputConfirmed')


    def __init__(self):
        """
        Constructor of the class
        """
        super(InputDialog, self).__init__()
        self.setupUi(self)
        self.number_of_transition_functions = 1
        self.max_states = 9
        self.current_mc_type = None
        self.systemSpecificationDialog = None
        self.initialization()


    def initialization(self):
        """
        Method for initializing the graphical interface
        """
        self.setWindowIcon(QtGui.QIcon('resources/icons/FS4DTMC.png'))
        self.set_conditional_visualization()
        self.tw_input.currentChanged.connect(self.set_conditional_visualization)
        self.rb_defineMC_ca.clicked.connect(self.set_conditional_visualization)
        self.rb_load_ca.clicked.connect(self.set_conditional_visualization)
        self.rb_defineMC_fa.clicked.connect(self.set_conditional_visualization)
        self.rb_load_fa.clicked.connect(self.set_conditional_visualization)
        self.cb_stateDesignations_ca.clicked.connect(self.set_conditional_visualization)
        self.cb_stateDesignations_fa.clicked.connect(self.set_conditional_visualization)
        self.cb_matrixDimension_ca.currentIndexChanged.connect(self.set_conditional_visualization)
        self.bu_filePath_ca.clicked.connect(self.set_CA_path)
        self.bu_filePath_fa.clicked.connect(self.set_FA_path)
        self.bu_reset_fa.clicked.connect(self.reset_mc_spezification)
        self.systemSpecificationDialog = SystemSpecificationDialog()
        self.bu_generateMCbySystem_fa.clicked.connect(self.generate_factor_distribution)
        self.create_transition_function('Transition function 1')
        self.tw_transitionFunction.currentChanged.connect(self.change_transition_function_tab)
        self.bb_inputDialog.accepted.connect(self.add_markov_chain)
        self.tw_transitionFunction.currentChanged.connect(self.set_conditional_visualization)
        self.te_factorDim0.textChanged.connect(self.update_factor0)
        self.te_factorDim1.textChanged.connect(self.update_factor1)
        self.te_factorDim2.textChanged.connect(self.update_factor2)



        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/icons/new_project.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tw_transitionFunction.addTab(QtWidgets.QWidget(), icon, 'Add transition function')


    def add_markov_chain(self):
        """
        Method that allows the creation of a new Markov chain
        :return:
        """
        mc_type = self.get_mc_type()
        if mc_type == "conventional":
            self.mcInputConfirmed.emit(mc_type,
                                              self.get_conventional_input(),
                                              self.outsourced_definition())

        elif mc_type == "forward":
            self.mcInputConfirmed.emit(mc_type,
                                       self.get_forward_input(),
                                    self.outsourced_definition())

    def get_mc_type(self):
        """
        Method to get the type of the Markov chain beeing created
        :return: Markov chain type
        """
        if self.tw_input.currentWidget() == self.tab_ConvApproach:
            return "conventional"
        elif self.tw_input.currentWidget() == self.tab_ForwardApproach:
            return "forward"
        else:
            raise NotImplementedError("This definition is not supported")


    def get_conventional_input(self):
        """
        Method to get the input of a conventional specified Markov chain
        :return: conventional MC configuration
        """
        configuration = {"Initial state vector": self._get_initial_state_vector(),
                         "Transition matrix": self._get_transition_matrix()
                         }
        if self.cb_stateDesignations_ca.isChecked():
            configuration["State designations"] = self._get_state_designations()
        else:
            configuration["State designations"] = None
        return configuration

    def _get_state_designations(self):
        """
        Method to get the optional state designation input
        :return: state designations
        """
        if self.cb_stateDesignations_ca.isChecked():
            state_designations = []
            max_states = self._get_max_states()
            dimension = self._get_matrix_dimension()
            for state in range(dimension):
                state_designations.append(getattr(self, 'le_stateDesignation_ca_{state}'
                                                    .format(state=(max_states - state))).text())
            state_designations.reverse()
        else:
            return None
        return state_designations

    def _get_initial_state_vector(self):
        """
        Method to get the input probabilities at system initialization
        :return: initial state vector
        """
        initial_state_vector = []
        max_states = self._get_max_states()
        dimension = self._get_matrix_dimension()
        for state in range(dimension):
            initial_state_vector.append(getattr(self, 'le_initialStateVector_ca_{state}'
                                                .format(state=(max_states - state))).text())
        initial_state_vector.reverse()
        return initial_state_vector

    def _get_transition_matrix(self):
        """
        Method to get the transition matrix
        :return: transition matrix
        """
        max_states = self._get_max_states()
        dimension = self._get_matrix_dimension()
        transition_matrix = []
        for state in range(dimension):
            transition_probabilities = []
            for con_state in range(dimension):
                transition_probabilities.append(getattr(self, 'le_transitionMatrix_ca_{state}{con_state}'.format(state=state,
                                                                                 con_state=
                                                                                 (max_states - con_state))).text())
            transition_probabilities.reverse()
            transition_matrix.append(transition_probabilities)
        return transition_matrix

    def get_forward_input(self):
        """
        Method to get the input of functional specified markoc chain
        :return: Markov chain configuration
        """
        if self.outsourced_definition():
            return {}
        else:
            configuration = {}
            configuration["States"] = []
            configuration["States"].append(self.te_stateSpace1_fa.text())
            configuration["States"].append(self.te_stateSpace2_fa.text())
            configuration["States"].append(self.te_stateSpace3_fa.text())
            configuration["State space names"] = []
            configuration["State space names"].append(self.te_stateDim0.toPlainText())
            configuration["State space names"].append(self.te_stateDim1.toPlainText())
            configuration["State space names"].append(self.te_stateDim2.toPlainText())
            if self.te_stateDesignations_fa.text() == "None":
                configuration["State designations"] = None
            else:
                configuration["State designations"] = [self.te_stateDesignations_fa.text()]
            configuration["Initial state vector"] = [self.te_initialStateVector_fa.text()]
            configuration["Factors"] = []
            configuration["Factors"].append(self.te_factors1_fa.text())
            configuration["Factors"].append(self.te_factors2_fa.text())
            configuration["Factors"].append(self.te_factors3_fa.text())
            configuration["Factor space names"] = []
            configuration["Factor space names"].append(self.te_factorDim0.toPlainText())
            configuration["Factor space names"].append(self.te_factorDim1.toPlainText())
            configuration["Factor space names"].append(self.te_factorDim2.toPlainText())
            configuration["Factor probabilities"] = []
            configuration["Factor probabilities"].append(self.te_factorsProbabilities1_fa.text())
            configuration["Factor probabilities"].append(self.te_factorsProbabilities2_fa.text())
            configuration["Factor probabilities"].append(self.te_factorsProbabilities3_fa.text())
            configuration["Transition functions"] = self._get_transition_functions()
        return configuration



    def _get_transition_functions(self):
        """
        Method to get the transition functions of the functional Markov chain specification
        :return: transition functions
        """
        transition_functions = []
        for index in range(self.number_of_transition_functions):
            transition_function = ''
            self.tw_transitionFunction.setCurrentIndex(index)
            transition_function += self.tw_transitionFunction.currentWidget().layout().itemAt(0).widget().get_transition_function_name()
            transition_function += "\n    "
            lines = self.tw_transitionFunction.currentWidget().layout().itemAt(0) \
                .widget().get_transition_function().split("\n")
            transition_function += "\n    ".join(lines)
            transition_function += '\n \n'
            transition_functions.append(transition_function)
        return transition_functions

    def set_mc_spezification(self, states: np.ndarray, state_designations: list, initial_state_vector: np.ndarray, factors: np.ndarray,
                             factor_distributions: np.ndarray, transition_functions: list, file_path: str=None):
        """
        Method to set the Markov chain specification
        :param states: state space of the MC
        :param state_designations: optional state designations
        :param initial_state_vector: vector of the initial state probabilities
        :param factors: vector of factors
        :param factor_distributions: vector of factor probabilities
        :param transition_functions: list of transition functions
        :param file_path: file path of alternative Markov chain specification on file
        :return:
        """
        if isinstance(states, str):
            self.reset()
            self.te_stateSpace1_fa.setText(states)
        else:
            if len(states) >= 1:
                self.te_stateSpace1_fa.setText(str(list(states[0])).replace("[", "").replace("]", ""))
            if len(states) >= 2:
                self.te_stateSpace2_fa.setText(str(list(states[1])).replace("[", "").replace("]", ""))
            if len(states) >= 3:
                self.te_stateSpace3_fa.setText(str(list(states[2])).replace("[", "").replace("]", ""))
        if isinstance(state_designations, str):
            self.te_stateDesignations_fa.setText(state_designations)
        else:
            self.te_stateDesignations_fa.setText(str(list(state_designations)).replace("[", "").replace("]", ""))
        if isinstance(initial_state_vector, str):
            self.te_initialStateVector_fa.setText(initial_state_vector)
        else:
            self.te_initialStateVector_fa.setText(str(list(initial_state_vector)).replace("[", "").replace("]", ""))
        if isinstance(factors, str):
            self.te_factors1_fa.setText(str(factors))
        else:
            factors = factors[0]
            if len(states) >= 1:
                self.te_factors1_fa.setText(str(list(factors[0])).replace("[", "").replace("]", ""))
            if len(states) >= 2:
                self.te_factors2_fa.setText(str(list(factors[1])).replace("[", "").replace("]", ""))
            if len(states) >= 3:
                self.te_factors3_fa.setText(str(list(factors[2])).replace("[", "").replace("]", ""))
        if isinstance(factor_distributions, str):
            self.te_factorsProbabilities1_fa.setText(str(factor_distributions).replace("[", "").replace("]", ""))
        else:
            factor_distributions = factor_distributions[0]
            if len(states) >= 1:
                self.te_factorsProbabilities1_fa.setText(str(list(factor_distributions[0])).replace("[", "").replace("]", ""))
            if len(states) >= 2:
                self.te_factorsProbabilities2_fa.setText(str(list(factor_distributions[1])).replace("[", "").replace("]", ""))
            if len(states) == 3:
                self.te_factorsProbabilities3_fa.setText(str(list(factor_distributions[0])).replace("[", "").replace("]", ""))
        for index in range(len(transition_functions)):
            self.tw_transitionFunction.setCurrentIndex(index)
            transition_functions_name = (transition_functions[index]).splitlines()[0]
            transition_functions[index] = "\n".join(transition_functions[index].splitlines()[1:])
            self.tw_transitionFunction.setCurrentIndex(index)
            self.tw_transitionFunction.currentWidget().layout().itemAt(0)
            self.tw_transitionFunction.currentWidget().layout().itemAt(0) \
                .widget().set_function(transition_functions_name, transition_functions[index], index)
        if file_path is None:
            self.rb_defineMC_fa.setChecked(True)
        else:
            self.rb_load_fa.setChecked(True)
            self.le_filePath_fa.setText(file_path)
        self.set_conditional_visualization()

    def outsourced_definition(self):
        """
        Method to get information if the Markov chain is specified in a GUI dialog of external file
        :return: outsourced definition
        """
        if self.get_mc_type() == "conventional":
            return self.rb_load_ca.isChecked()

        else:
            return self.rb_load_fa.isChecked()

    def get_input_file_path(self):
        """
        Method to get the file path of the outsourced input file
        :return: input file path
        """
        if self.get_mc_type() == "conventional":
            return self.le_filePath_ca.text()
        else:
            return self.le_filePath_fa.text()

    def set_current_mc_type(self, type: str):
        """
        Method to get the type of the confirmed Markoc chain
        :param type: Markov chain type
        """
        self.current_mc_type = type

    def set_FA_path(self):
        """
        Method to set the path of the Markov chain input of functional specified Markov chains
        :return: input file path
        """
        file_path = self.set_path()
        self.le_filePath_fa.setText(file_path)

    def set_CA_path(self):
        """
        Method to set the path of the Markov chain input of conventional specified Markov chains
        :return: input file path
        """
        file_path = self.set_path()
        self.le_filePath_ca.setText(file_path)

    def set_path(self):
        """
        method to set the paths of Markov chains
        :return: input file path
        """
        return QFileDialog.getOpenFileName(None, 'Open file',
                                           './resources/configuration_files/', "*.json")[0]

    def change_transition_function_tab(self):
        """
        Method to change the tab of the transition functions
        """
        if self.tw_transitionFunction.currentIndex() == 3:
            self.tw_transitionFunction.setCurrentIndex(2)
        if self.tw_transitionFunction.currentIndex() == self.number_of_transition_functions:
            self.number_of_transition_functions += 1
            self.create_transition_function('Transition function {functionNumber}'
                            .format(functionNumber=self.number_of_transition_functions))


    def create_transition_function(self, tf_name):
        """
        Mthod to create a new transition function in a new tab
        :param tf_name: name of the transition function
        """
        if self.number_of_transition_functions < 4:
            newTF = QtWidgets.QWidget()
            newTF.setObjectName(tf_name)
            self.tw_transitionFunction.insertTab(self.tw_transitionFunction.currentIndex(),
                                                  newTF,
                                                  newTF.objectName()
                                                  )

            tf_layout = QtWidgets.QVBoxLayout()
            if self.tw_transitionFunction.currentIndex() == 0:
                tf = TransitionFunction()
            else:
                tf = TransitionFunction(self.tw_transitionFunction.currentIndex())
            tf_layout.addWidget(tf)
            newTF.setLayout(tf_layout)
            self.tw_transitionFunction.setCurrentIndex(self.tw_transitionFunction.currentIndex() - 1)
        else:
            self.tw_transitionFunction.setCurrentIndex(2)




    def generate_factor_distribution(self):
        """
        method to open a dialog for factor creation
        """
        self.systemSpecificationDialog.exec()

    def visualize_distributions(self, arrival_time_distribution,batch_size_distribution):
        """
        Method to visualize the input distributions
        :param arrival_time_distribution: plot of the arrival time
        :param batch_size_distribution: plot of the batch size
        :return:
        """
        self.systemSpecificationDialog.visualize_distributions(arrival_time_distribution, batch_size_distribution)

    def _get_max_states(self):
        """
        Get the maximum number of visualizable states
        :return: max_states
        """
        return self.max_states

    def _get_matrix_dimension(self):
        """
        method to get the dimension of the input matrix
        :return: matrix dimension
        """
        dimensions = {"2 x 2 Matrix":    2,
                      "3 x 3 Matrix":    3,
                      "4 x 4 Matrix":    4,
                      "5 x 5 Matrix":    5,
                      "6 x 6 Matrix":    6,
                      "7 x 7 Matrix":    7,
                      "8 x 8 Matrix":    8,
                      "9 x 9 Matrix":    9,
                      "10 x 10 Matrix": 10
                      }
        return dimensions[self.cb_matrixDimension_ca.currentText()]


    def reset_mc_spezification(self):
        """
        Method that allows to reset the windows input fields
        """
        for i in range(1,self.number_of_transition_functions):
            self.tw_transitionFunction.removeTab(1)
        self.number_of_transition_functions = 1
        self.tw_transitionFunction.setCurrentIndex(0)
        self.set_conditional_visualization()

        self.te_stateSpace1_fa.setText("")
        self.te_stateSpace2_fa.setText("")
        self.te_stateSpace3_fa.setText("")

        self.te_initialStateVector_fa.setText("")
        self.te_stateDesignations_fa.setText("")

        self.te_factors1_fa.setText("")
        self.te_factors2_fa.setText("")
        self.te_factors3_fa.setText("")

        self.te_factorsProbabilities1_fa.setText("")
        self.te_factorsProbabilities2_fa.setText("")
        self.te_factorsProbabilities3_fa.setText("")

        self.le_filePath_fa.setText("C://")

    def update_factor0(self):
        """
        Method that allows to update the name of factor space0
        """
        self.te_factorDim0_prob.setText(self.te_factorDim0.toPlainText())

    def update_factor1(self):
        """
        Method that allows to update the name of factor space1
        """
        self.te_factorDim1_prob.setText(self.te_factorDim1.toPlainText())

    def update_factor2(self):
        """
        Method that allows to update the name of factor space2
        """
        self.te_factorDim2_prob.setText(self.te_factorDim2.toPlainText())

    def reset(self):
        """
        Method that allows to reset the window
        :return:
        """
        self._reset_conventional_approach()
        self._reset_forward_approach()



    def _reset_conventional_approach(self):
        """
        Method that allows to reset the tab for conventional specified Markov chains
        """
        max_states = self._get_max_states()
        for state in range(max_states+1):
            getattr(self, 'le_stateDesignation_ca_{state}'.format(state=state)).setVisible(False)
            getattr(self, 'le_stateDesignation_ca_{state}'.format(state=state)).setEnabled(False)
            getattr(self, 'le_initialStateVector_ca_{state}'.format(state=state)).setVisible(False)
            getattr(self, 'le_initialStateVector_ca_{state}'.format(state=state)).setEnabled(False)
            for con_state in range(max_states+1):
                getattr(self, 'le_transitionMatrix_ca_{state}{con_state}'.format(state=state,
                                                                                 con_state=con_state))\
                    .setVisible(False)
                getattr(self, 'le_transitionMatrix_ca_{state}{con_state}'.format(state=state,
                                                                                 con_state=con_state)) \
                    .setEnabled(False)
        self.le_filePath_ca.setEnabled(False)
        self.bu_filePath_ca.setEnabled(False)

    def _reset_forward_approach(self):
        """
        Method that allows to reset the tab for functional specified Markov chains
        """
        self.te_stateSpace1_fa.setEnabled(False)
        self.te_stateSpace2_fa.setEnabled(False)
        self.te_stateSpace3_fa.setEnabled(False)
        self.te_stateDesignations_fa.setEnabled(False)
        self.te_factors1_fa.setEnabled(False)
        self.te_factors2_fa.setEnabled(False)
        self.te_factors3_fa.setEnabled(False)
        self.te_factorsProbabilities1_fa.setEnabled(False)
        self.te_factorsProbabilities2_fa.setEnabled(False)
        self.te_factorsProbabilities3_fa.setEnabled(False)
        self.te_initialStateVector_fa.setEnabled(False)
        self.tw_transitionFunction.setEnabled(False)
        self.le_filePath_fa.setEnabled(False)
        self.bu_filePath_fa.setEnabled(False)

        self.te_stateSpace2_fa.setVisible(False)
        self.te_stateSpace3_fa.setVisible(False)
        self.te_factors2_fa.setVisible(False)
        self.te_factors3_fa.setVisible(False)
        self.te_factorsProbabilities2_fa.setVisible(False)
        self.te_factorsProbabilities3_fa.setVisible(False)
        self.te_stateSpace2_fa.setVisible(False)
        self.te_stateSpace3_fa.setVisible(False)
        self.te_factors2_fa.setVisible(False)
        self.te_factors3_fa.setVisible(False)
        self.te_factorsProbabilities2_fa.setVisible(False)
        self.te_factorsProbabilities3_fa.setVisible(False)
        self.te_stateDim1.setVisible(False)
        self.te_factorDim1.setVisible(False)
        self.te_factorDim1_prob.setVisible(False)
        self.te_stateDim2.setVisible(False)
        self.te_factorDim2.setVisible(False)
        self.te_factorDim2_prob.setVisible(False)



    def set_conditional_visualization(self):
        """
        Method to set the conventional visualization depending on the previous input
        """
        self.reset()

        if self.current_mc_type == "MarkovChainConventionalApproach":
            self.tw_input.setCurrentIndex(0)

        elif self.current_mc_type == "MarkovChainForwardApproach":
            self.tw_input.setCurrentIndex(1)

        if self.tw_input.currentIndex() == 0:
            max_states = self._get_max_states()
            dimension = self._get_matrix_dimension()
            for state in range(dimension):
                getattr(self, 'le_stateDesignation_ca_{state}'.format(state=(max_states - state))).setVisible(True)
                getattr(self, 'le_initialStateVector_ca_{state}'.format(state=(max_states - state))).setVisible(True)
                for con_state in range(dimension):
                    getattr(self, 'le_transitionMatrix_ca_{state}{con_state}'.format(state=state,
                                                                                       con_state=
                                                                                       (max_states - con_state))) \
                        .setVisible(True)
            if self.rb_defineMC_ca.isChecked():
                for state in range(dimension):
                    getattr(self, 'le_initialStateVector_ca_{state}'.format(state=(max_states - state))).setEnabled(True)
                    for con_state in range(dimension):
                        getattr(self, 'le_transitionMatrix_ca_{state}{con_state}'.format(state=state,
                                                                                         con_state=
                                                                                         (max_states - con_state))) \
                            .setEnabled(True)

                if self.cb_stateDesignations_ca.isChecked():
                    for state in range(dimension):
                        getattr(self, 'le_stateDesignation_ca_{state}'.format(state=(max_states-state))).setEnabled(True)



            elif self.rb_load_ca.isChecked():
                self.le_filePath_ca.setEnabled(True)
                self.bu_filePath_ca.setEnabled(True)

        else:
            if self.rb_defineMC_fa.isChecked():
                self.te_stateSpace1_fa.setEnabled(True)
                self.te_factors1_fa.setEnabled(True)
                self.te_factorsProbabilities1_fa.setEnabled(True)
                self.te_stateSpace2_fa.setEnabled(True)
                self.te_factors2_fa.setEnabled(True)
                self.te_factorsProbabilities2_fa.setEnabled(True)
                self.te_stateSpace3_fa.setEnabled(True)
                self.te_factors3_fa.setEnabled(True)
                self.te_factorsProbabilities3_fa.setEnabled(True)
                self.te_initialStateVector_fa.setEnabled(True)
                self.tw_transitionFunction.setEnabled(True)
                if self.number_of_transition_functions >= 2:
                    self.te_stateSpace2_fa.setVisible(True)
                    self.te_factors2_fa.setVisible(True)
                    self.te_factorsProbabilities2_fa.setVisible(True)
                    self.te_stateDim1.setVisible(True)
                    self.te_factorDim1.setVisible(True)
                    self.te_factorDim1_prob.setVisible(True)
                    if self.number_of_transition_functions == 3:
                        self.te_stateSpace3_fa.setVisible(True)
                        self.te_factors3_fa.setVisible(True)
                        self.te_factorsProbabilities3_fa.setVisible(True)
                        self.te_stateDim2.setVisible(True)
                        self.te_factorDim2.setVisible(True)
                        self.te_factorDim2_prob.setVisible(True)



                if self.cb_stateDesignations_fa.isChecked():
                    self.te_stateDesignations_fa.setEnabled(True)
                else:
                    self.te_stateDesignations_fa.setText("None")


            elif self.rb_load_fa.isChecked():
                self.le_filePath_fa.setEnabled(True)
                self.bu_filePath_fa.setEnabled(True)


