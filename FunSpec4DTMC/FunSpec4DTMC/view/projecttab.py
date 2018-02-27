
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

from  PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog
from matplotlib.backends.backend_qt5agg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar)
import time
import numpy as np
from FunSpec4DTMC.view.ui_projecttab import Ui_ProjectTab
from FunSpec4DTMC.view.inputdialog import InputDialog
from FunSpec4DTMC.view.functionalinput import FunctionalInput
from FunSpec4DTMC.view.strategyselectiondialog import StrategySelectionDialog


class ProjectTab(QDialog, Ui_ProjectTab):

    def __init__(self):
        """
        Constructor of the class ProjectTab
        """
        super(ProjectTab, self).__init__()
        self.inputDialog = None
        # Set up the user interface created by the Qt Designer.
        self.setupUi(self)
        self._initialization()


    def _initialization(self):
        """
        Method to initialize the graphical interface
        """
        self.inputDialog = InputDialog()
        self.strategySelectionDialog = StrategySelectionDialog()
        self._cancel_analysis = False
        self._bind_signals()
        self.scrollArea.setVisible(False)

    def _bind_signals(self):
        """
        Method to bind signals to the widgets of the graphical interface
        """
        self.pushButton_addMC.clicked.connect(self.set_markov_chain)
        self.pushButton_chMethod.clicked.connect(self.choose_strategy)
        self.pushButton_cancelAnalysis.clicked.connect(self.cancel_analysis)

    def set_markov_chain(self):
        """
        Method to start the Markov chain definition dialoque
        """
        self.inputDialog.set_conditional_visualization()
        self.inputDialog.exec()

    def choose_strategy(self):
        """
        Method to start the strategy selection dialoque
        """
        self._cancel_analysis = False
        self.strategySelectionDialog.set_conditional_visualisation()
        self.strategySelectionDialog.exec()

    def set_current_mc_type(self, type: str):
        """
        Method to set the current Markov chain type
        :param type:
        :return:
        """
        self.inputDialog.set_current_mc_type(type)
        self.strategySelectionDialog.set_current_mc_type(type)

    def get_input_file_path(self):
        """
        method to get the input file path
        :return: input file path
        """
        return self.inputDialog.get_input_file_path()

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
        self.inputDialog.set_mc_spezification(states, state_designations, initial_state_vector,
                                              factors, factor_distributions, transition_functions, file_path)

    def visualize_distributions(self, arrival_time_distribution, batch_size_distribution):
        """
        Method to visualize the input distributions
        :param arrival_time_distribution: plot of the arrival time distribution
        :param batch_size_distribution: plot of the batch size distribution
        """
        self.inputDialog.visualize_distributions(arrival_time_distribution, batch_size_distribution)

    def enable_simulation(self):
        """
        Method to enable the simulation in the GUI
        """
        self.pushButton_chMethod.setEnabled(True)
        self.pushButton_cancelAnalysis.setEnabled(True)

    def cancel_analysis(self):
        """
        Method to initiate the analysis termination
        """
        self._cancel_analysis = True

    def visualize_input(self, input_plots: list):
        """
        Method to visualize the handed over input
        :param input_plots:
        """
        self.tabWidget_inputVisualisation.clear()
        for mc in input_plots:
            newTab = QtWidgets.QWidget()
            newTab.setObjectName("Markov chain {mcNumber}"
                                 .format(mcNumber=self.tabWidget_inputVisualisation.count() + 1))

            if type(mc) is tuple:
                functional_input = FunctionalInput()
                layout_isv = QtWidgets.QVBoxLayout()
                layout_isv.addWidget(FigureCanvas(mc[0]))
                functional_input.wid_initialStateVector.setLayout(layout_isv)
                layout_factors = QtWidgets.QVBoxLayout()
                layout_factors.addWidget(FigureCanvas(mc[1]))
                functional_input.wid_factorDistribution.setLayout(layout_factors)
                functional_input.add_transition_function(mc[2])
                functional_layout = QtWidgets.QVBoxLayout()
                functional_layout.addWidget(functional_input)
                newTab.setLayout(functional_layout)


            else:
                tab_layout = QtWidgets.QVBoxLayout()
                tab_layout.addWidget(FigureCanvas(mc))
                newTab.setLayout(tab_layout)

            self.tabWidget_inputVisualisation.insertTab(self.tabWidget_inputVisualisation.count() + 1,
                                                            newTab,
                                                            newTab.objectName()
                                                            )

    def clear_results(self):
        """
        Method to clear the result visualization
        :return:
        """
        self.tabWidget_resultVisualisation.clear()

    def clear_input(self):
        """
        Method to clear the input visualization
        """
        self.tabWidget_inputVisualisation.clear()

    def visualize_results(self, result: list, title: list):
        """
        Method to vislalize the results in the GUI
        :param result: resulting Plots
        :param title: titles of the Plots
        :return:
        """
        new_tab = QtWidgets.QWidget()
        verticalLayout_results = QtWidgets.QVBoxLayout()
        verticalLayout_results.setObjectName("verticalLayout_results")


        canvas = FigureCanvas(result)
        verticalLayout_results.addWidget(canvas)
        toolbar = NavigationToolbar(canvas,
                                    self, coordinates=True)
        verticalLayout_results.addWidget(toolbar)
        new_tab.setLayout(verticalLayout_results)
        self.tabWidget_resultVisualisation.addTab(new_tab, title)


    def update_calculation_characteristics(self, steps: int, norm: float):
        """
        Method to update the calculation caracteristivs in the GUI
        :param steps: Current iteration step
        :param norm: current difference of the consecutive state vectors in norm
        :return:
        """
        self.le_currentStep.setText(str(steps))
        self.le_currentPrecision.setText(str(norm))
        QtCore.QCoreApplication.processEvents()
        if self._cancel_analysis:
            self._cancel_analysis = False
            raise KeyboardInterrupt
        time.sleep(0.01)

