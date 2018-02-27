
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

import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from FunSpec4DTMC.view.ui_mainwindow import Ui_MainWindow
from FunSpec4DTMC.view.projecttab import ProjectTab
from FunSpec4DTMC.view.precisionSelectionDialog import PrecisionSelectionDialog
from FunSpec4DTMC.view.dicretizationPrecisionSelectionDialog import DiscretizationPrecisionSelectionDialog
from FunSpec4DTMC.view.displayPrecisionSelectionDialog import DisplayPrecisionSelectionDialog
from FunSpec4DTMC.view.ErrorDialogs.calculationerror import CalculationError
from FunSpec4DTMC.view.ErrorDialogs.inputfileerror import InputFileError
from FunSpec4DTMC.view.ErrorDialogs.inputerror import InputError
from FunSpec4DTMC.view.ErrorDialogs.runtimeWarning import RuntimeWarning
from PyQt5.QtWidgets import QFileDialog


class MainWindow(QMainWindow, Ui_MainWindow):
    saveDialogOpened = pyqtSignal(str, int, name='saveDialogOpened')
    modeSelected = pyqtSignal(bool, bool, name='modeSelected')
    strategySelected = pyqtSignal(str, int, float, int, dict, str, str, name='strategySelected')
    persistenceSet = pyqtSignal(bool, name='persistenceSet')
    projectChanged = pyqtSignal(int, name='projectCreated')
    mcInputConfirmed = pyqtSignal(str, dict, bool,
                                   name='mcDefinitionConfirmed')
    systemVisualizationTriggered = pyqtSignal(str, tuple,  bool, name='systemVisualizationTriggered')
    systemInputProcessingTriggered = pyqtSignal(str, tuple, bool, bool, name='systemInputProcessingTriggered')
    calculationPrecisionAdjusted = pyqtSignal(float, name='calculationPrecisionAdjusted')
    discretizationPrecisionAdjusted = pyqtSignal(float, name='discretizationPrecisionAdjusted')
    displayPrecisionAdjusted = pyqtSignal(int, name='displayPrecisionAdjusted')
    ignoreInputVisualization = pyqtSignal(bool, name='ignoreInputVisualisation')

    def __init__(self):
        """
        Constructor of the class MainWindow
        """
        super(MainWindow, self).__init__()

        # Set up the user interface created by the Qt Designer.
        self.setupUi(self)
        self.numberOfTabs = 1
        self.currentProjectTab = ProjectTab()
        self.initialization()
        self.projects = []

    def initialization(self):
        """
        Method to initialize the graphical interface
        """
        self.setWindowIcon(QtGui.QIcon('resources/icons/FS4DTMC.png'))
        self.QActionGroupCython = QtWidgets.QActionGroup(self)
        self.QActionGroupCython.addAction(self.actionCythonMode)
        self.QActionGroupCython.addAction(self.actionPythonMode)
        self.QActionGroupInputVis = QtWidgets.QActionGroup(self)
        self.QActionGroupInputVis.addAction(self.actionTrue)
        self.QActionGroupInputVis.addAction(self.actionFalse)
        self.QActionGroupPersistence = QtWidgets.QActionGroup(self)
        self.QActionGroupPersistence.addAction(self.actionDiscard_plots_of_past_simulations)
        self.QActionGroupPersistence.addAction(self.actionDisplay_plots_of_previous_simulations)
        self.QActionGroupResearch = QtWidgets.QActionGroup(self)
        self.QActionGroupResearch.addAction(self.actionResearchUsage)
        self.QActionGroupResearch.addAction(self.actionTeachingUsage)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resources/icons/new_project.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newProject = QtWidgets.QWidget()
        self.newProject.setObjectName("newProject")
        self.numberOfTabs += 1
        self.tabWidgetMainWindow.addTab(self.newProject, icon, "New Project")
        self.actionSave.setShortcut('CTRL+S')
        self.precisionSelectionDialog = PrecisionSelectionDialog()
        self.discretizationPrecisionSelectionDialog = DiscretizationPrecisionSelectionDialog()
        self.displayPrecisionDialog = DisplayPrecisionSelectionDialog()
        self.bind_slots()

        # Bind Slots

    def bind_slots(self):
        """
        Method to bind signals to the widgets of the graphical interface
        """
        self.tabWidgetMainWindow.currentChanged.connect(self._tab_switched)
        self.actionSave.triggered.connect(self.save_mc)
        self.actionSet_calculation_precision.triggered.connect(self._select_calculation_precision)
        self.actionSet_display_accuracy.triggered.connect(self._select_display_precision)
        self.actionSet_discretization_precision.triggered.connect(self._select_discretization_precision)
        self.actionPythonMode.toggled.connect(self.set_mode)
        self.actionTrue.toggled.connect(self.adapt_input_visualization)
        self.actionResearchUsage.toggled.connect(self.set_mode)
        self.actionDisplay_plots_of_previous_simulations.toggled.connect(self.set_persistence)
        self.activate_new_projects_slots()

    def activate_new_projects_slots(self):
        """
        Method to activate the slots of the new project
        """
        self.currentProjectTab.strategySelectionDialog.strategySelected.connect(self.strategySelected.emit)
        self.currentProjectTab.inputDialog.systemSpecificationDialog.systemInputProcessingTriggered.connect(
            self.systemInputProcessingTriggered.emit)
        self.currentProjectTab.inputDialog.systemSpecificationDialog.systemVisualizationTriggered. \
            connect(self.systemVisualizationTriggered.emit)
        self.precisionSelectionDialog.calculationPrecisionAdjusted.connect(self.calculationPrecisionAdjusted.emit)
        self.discretizationPrecisionSelectionDialog.discretizationPrecisionAdjusted.connect(self.discretizationPrecisionAdjusted.emit)
        self.displayPrecisionDialog.displayPrecisionAdjusted.connect(self.displayPrecisionAdjusted.emit)
        self.currentProjectTab.inputDialog.mcInputConfirmed.connect(self.mcInputConfirmed.emit)



    def save_mc(self):
        """
        Interface method used to save the current Markov chain using a dile dialoque
        """
        fp = QFileDialog.getSaveFileName(QFileDialog(), 'Select storage path',
                                         './resources/configuration_files/', "*.json")[0]
        self.saveDialogOpened.emit(fp, self.currentProjectTab.tabWidget_inputVisualisation.currentIndex())

    def start_gui(self):
        """
        Interface method to start and show the GUI
        """
        self.show()
        self.new_project()
        self.showFullScreen()
        self.showMaximized()


    def set_mode(self):
        """
        Interface method to adjust the mode. Selection between Cython and Python mode
        """
        if self.actionPythonMode.isChecked():
            cythonMode=False
        else:
            cythonMode=True
        if self.actionResearchUsage.isChecked():
            researchMode=True
        else:
            researchMode=False

        self.modeSelected.emit(cythonMode, researchMode)

    def set_persistence(self):
        """
        Interface method to set the persistence of the visualized results
        """
        self.persistenceSet.emit(self.actionDisplay_plots_of_previous_simulations.isChecked())

    def adapt_input_visualization(self):
        """
        Interface method to select if the input visualization is omitted
        """
        self.ignoreInputVisualization.emit(self.actionTrue.isChecked())

    def clear_results(self):
        """
        Interface method to clear the visualized input
        """
        self.currentProjectTab.clear_results()

    def clear_input(self):
        """
        Interface method to clear the visualized input
        """
        self.currentProjectTab.clear_input()

    def enableCythonMode(self, enabled: bool):
        """
        Interface method to enable the selection of the cython mode
        """
        self.actionCythonMode.setEnabled(enabled)

    def new_project(self):
        """
        Method to initialize a new project
        """
        self._generate_new_project_tab()

    def enable_saving(self):
        """
        Method to enable the possibility of saving a markov chain to disk
        :return:
        """
        self.actionSave.setEnabled(True)

    def enable_simulation(self):
        """
        method that enables the simulation possibilities in GUI
        """
        self.currentProjectTab.enable_simulation()

    def visualize_input(self, input_plots: list):
        """
        Interface method for input visualization
        :param input_plots: list of plots of the Markoc chain input
        :return:
        """
        self.currentProjectTab.visualize_input(input_plots)

    def get_input_file_path(self):
        """
        Interface method to get the file path of the input
        :return: input file path
        """
        return self.currentProjectTab.get_input_file_path()

    def visualize_results(self, results: list, title: list):
        """
        Interface method for the visualization of the resulting metrics
        :param results: list of resulting plots
        :param title: list of the plot titles
        """
        self.currentProjectTab.visualize_results(results, title)

    def set_mc_spezification(self, states: np.ndarray, state_designations: list, initial_state_vector: np.ndarray,
                             factors: np.ndarray,
                             factor_distributions: np.ndarray, transition_functions: list, file_path: str = None):
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
        self.currentProjectTab.set_mc_spezification(states, state_designations, initial_state_vector,
                                                    factors, factor_distributions, transition_functions, file_path)

    def visualize_distributions(self, arrival_time_distribution, batch_size_distribution):
        """
        Method to visualize the input distributions
        :param arrival_time_distribution: plot of the arrival time distribution
        :param batch_size_distribution: plot of the batch size distribution
        """
        self.currentProjectTab.visualize_distributions(arrival_time_distribution, batch_size_distribution)

    def set_current_project(self, project_number):
        """
        Method to select the current project number
        :param project_number: current project number
        :return:
        """
        self.currentProjectTab = self.projects[project_number]

    def set_current_mc_type(self, type):
        """
        Method to select the current Markov chain type
        :param type: tye of the Markov chain
        """
        self.currentProjectTab.set_current_mc_type(type)

    def update_calculation_characteristics(self, steps: int, norm: float):
        """
        Method to update the calculation caracteristivs in the GUI
        :param steps: Current iteration step
        :param norm: current difference of the consecutive state vectors in norm
        :return:
        """
        try:
            self.currentProjectTab.update_calculation_characteristics(steps, norm)
        except:
            raise InterruptedError

    def _tab_switched(self):
        """
        Method that emits a signal if the current tab switched
        """
        self.projectChanged.emit(self.tabWidgetMainWindow.currentIndex())

    def _select_calculation_precision(self):
        """
        Method to open a dialoque to adjust the calculation precision
        """
        self.precisionSelectionDialog.exec()

    def _select_display_precision(self):
        """
        Method to open a dialoque to adjust the display precision
        """
        self.displayPrecisionDialog.exec()

    def _select_discretization_precision(self):
        """
        Method to open a dialoque to adjust the discretization precision
        """
        self.discretizationPrecisionSelectionDialog.exec()

    def _generate_new_project_tab(self):
        """
        Method to create a new project tab
        """
        newTab = QtWidgets.QWidget()
        newTab.setObjectName("Project {projectNumber}"
                             .format(projectNumber=self.tabWidgetMainWindow.currentIndex() + 1))

        self.tabWidgetMainWindow.insertTab(self.tabWidgetMainWindow.currentIndex(),
                                           newTab,
                                           newTab.objectName()
                                           )

        tab_layout = QtWidgets.QVBoxLayout()
        self.currentProjectTab = ProjectTab()

        self.projects.append(self.currentProjectTab)
        tab_layout.addWidget(self.currentProjectTab)
        newTab.setLayout(tab_layout)
        self.tabWidgetMainWindow.setCurrentIndex(self.tabWidgetMainWindow.currentIndex() - 1)
        self.activate_new_projects_slots()

    def show_calculation_error_dialog(self):
        """
       Method to open the calculation error dialoque
        """
        error_dialog = CalculationError()
        error_dialog.exec()

    def show_input_file_error_dialog(self):
        """
        Method to open the file error dialoque
        """
        error_dialog = InputFileError()
        error_dialog.exec()

    def show_input_error_dialog(self):
        """
        Method to open the input error dialoque
        """
        error_dialog = InputError()
        error_dialog.exec()

    def input_visualization_aborted(self):
        self.runtime_warning = RuntimeWarning()
        return self.runtime_warning.exec(), self.runtime_warning.hiding_dialog()
