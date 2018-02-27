
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

from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QDialog
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import (
     FigureCanvasQTAgg as FigureCanvas,
     NavigationToolbar2QT as NavigationToolbar)
from PyQt5.QtWidgets import QFileDialog
from FunSpec4DTMC.view.transitionfunction import TransitionFunction
from FunSpec4DTMC.view.ui_systemSpecificationDialog import Ui_SystemSpezificationDialog


class SystemSpecificationDialog(QDialog, Ui_SystemSpezificationDialog):

    systemVisualizationTriggered = pyqtSignal(str, tuple, bool, name='systemVisualizationTriggered')
    systemInputProcessingTriggered = pyqtSignal(str, tuple, bool, bool, name='systemInputProcessingTriggered')

    def __init__(self):
        """
        Constructor of the class SystemSpecificationDialog
        """
        super(SystemSpecificationDialog, self).__init__()
        # Set up the user interface created by the Qt Designer.
        self._number_of_transition_functions = 1
        self.setupUi(self)
        self.initialization()
        self.create_transition_function('Transition function 1')
        self._number_of_transition_functions = 2
        self.create_transition_function('Transition function 2')
        self.cb_separateFactorDistributions.setChecked(True)

    def initialization(self):
        """
        Method for initialization of the graphical interface
        """
        self.setupSignals()
        self.setupGIGID1QmaxSystem()
        self.tw_transitionFunctions.setCurrentIndex(1)
        self.cb_separateFactorDistributions.clicked.connect(self.change_transition_function_tab)


    def setupGIGID1QmaxSystem(self):
        """
        Method to setup the interface for the input of a GI^GI/D/1-Q_MAX system
        """
        self._reset()
        self.canvas_arrivalTime = FigureCanvas(
            self._generate_empty_figure("A(t)", '$t/\Delta\ t$'))
        self.canvas_batchSize = FigureCanvas(
            self._generate_empty_figure("B(t)", '$t/\Delta\ t$'))
        self.toolbar_arrivalTime = NavigationToolbar(self.canvas_arrivalTime, self)
        self.hl_toolbarArrival.addWidget(self.toolbar_arrivalTime)

        self.toolbar_batchSize = NavigationToolbar(self.canvas_batchSize, self)
        self.hl_toolbarBatch.addWidget(self.toolbar_batchSize)
        self.wid_arrivalTimeDistributionFunction.layout().addWidget(self.canvas_arrivalTime)
        self.wid_batchSizeDistributionFunction.layout().addWidget(self.canvas_batchSize)


    def setupSignals(self):
        """
        Method to bind the signals to the graphical widgets of the interface
        :return:
        """
        self.cob_arrivalTimeDistribution.currentIndexChanged.connect(self._set_conditional_visualization)
        self.cob_batchSizeDistribution.currentIndexChanged.connect(self._set_conditional_visualization)
        self.bb_processingOperation.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(lambda:
                                                                                self.systemVisualizationTriggered.
                                                                                emit(self.get_system_designation(),
                                                                                     self.get_system_input(),
                                                                                     self._service_time_adjustment()))
        self.bb_processingOperation.accepted.connect(lambda:
                                                     self.systemInputProcessingTriggered.emit(
                                                            self.get_system_designation(),
                                                            self.get_system_input(),
                                                            self._service_time_adjustment(),
                                                            self._seperated_factors()))
        self.cb_maximumArrivalTime.clicked.connect(self._set_conditional_visualization)
        self.cb_maximumBatchSize.clicked.connect(self._set_conditional_visualization)
        self.rb_fileInputArrivalTime.clicked.connect(self._set_conditional_visualization)
        self.rb_fileInputBatchSize.clicked.connect(self._set_conditional_visualization)
        self.rb_listInputArrivalTime.clicked.connect(self._set_conditional_visualization)
        self.rb_listInputBatchSize.clicked.connect(self._set_conditional_visualization)
        self.bu_filePath_ArrivalTime.clicked.connect(self._set_ArrivalTime_path)
        self.bu_filePath_BatchSize.clicked.connect(self._set_BatchSize_path)



    def get_system_input(self):
        """
        method to get the input of the system specification
        """
        return (self._get_distribution("arrival"),
                self._get_distribution("batch"),
                self._get_service_time(),
                self._get_qmax(),
                self._get_transition_functions())

    def get_system_designation(self):
        """
        Method to get the system designation
        """
        if self.tw_system.currentIndex() == 0:
            return "GI^GI/D/1-Qmax"
        else:
            raise NotImplementedError



    def _get_distribution(self, type: str):
        """
        Method to determine the selected distribution
        :param type: type of the distribution
        :return: distribution
        """
        system_configuration = {}
        if type == "arrival":
            distribution = self.cob_arrivalTimeDistribution.currentText()
            system_configuration["name"] = distribution
            system_configuration["maximum"] = self.le_maximumArrivalTime.text()
        elif type == "batch":
            distribution = self.cob_batchSizeDistribution.currentText()
            system_configuration["name"] = distribution
            system_configuration["maximum"] = self.le_maximumBatchSize.text()
        else:
            raise NotImplementedError

        if distribution == "Exponential distribution":
            if type == "arrival":
                system_configuration["rate"] = self.le_rateArrivalTime.text()
            elif type == "batch":
                system_configuration["rate"] = self.le_rateBatchSize.text()
            else:
                raise NotImplementedError

        elif distribution == "K-Erlang distribution":
            if type == "arrival":
                system_configuration["rate"] = self.le_rateArrivalTime.text()
                system_configuration["k"] = self.le_kArrivalTime.text()
            elif type == "batch":
                system_configuration["rate"] = self.le_rateBatchSize.text()
                system_configuration["k"] = self.le_kBatchSize.text()
            else:
                raise NotImplementedError

        elif distribution == "Hyperexponential distribution":
            if type == "arrival":
                system_configuration["li"] = self.le_liArrivalTime.text()
                system_configuration["pi"] = self.le_piArrivalTime.text()
            elif type == "batch":
                system_configuration["li"] = self.le_liBatchSize.text()
                system_configuration["pi"] = self.le_piBatchSize.text()
            else:
                raise NotImplementedError

        elif distribution == "Gamma distribution":
            if type == "arrival":
                system_configuration["alpha"] = self.le_alphaArrivalTime.text()
                system_configuration["beta"] = self.le_betaArrivalTime.text()
            elif type == "batch":
                system_configuration["alpha"] = self.le_alphaBatchSize.text()
                system_configuration["beta"] = self.le_betaBatchSize.text()
            else:
                raise NotImplementedError

        elif distribution == "Uniform distribution":
            if type == "arrival":
                system_configuration["minimum"] = self.le_minArrivalTime.text()
                system_configuration["maximum"] = self.le_maxArrivalTime.text()
            elif type == "batch":
                system_configuration["minimum"] = self.le_minBatchSize.text()
                system_configuration["maximum"] = self.le_maxBatchSize.text()
            else:
                raise NotImplementedError

        elif distribution == "General independent distribution":
            if type == "arrival":
                if self.rb_listInputArrivalTime.isChecked():
                    system_configuration["input values"] = self.le_inputValuesArrivalTime.text()
                    system_configuration["probabilities"] = self.le_probabiliesArrivalTime.text()
                    system_configuration["path"] = None
                elif self.rb_fileInputArrivalTime.isChecked():
                    system_configuration["path"] = self.le_fileInputArrivalTime.text()
                    system_configuration["input values"] = None
                    system_configuration["probabilities"] = None
                else:
                    raise NotImplementedError

            elif type == "batch":
                if self.rb_listInputBatchSize.isChecked():
                    system_configuration["input values"] = self.le_inputValuesBatchSize.text()
                    system_configuration["probabilities"] = self.le_probabiliesBatchSize.text()
                    system_configuration["path"] = None
                elif self.rb_fileInputBatchSize.isChecked():
                    system_configuration["path"] = self.le_fileInputBatchSize.text()
                    system_configuration["input values"] = None
                    system_configuration["probabilities"] = None
                else:
                    raise NotImplementedError

        return system_configuration

    def change_transition_function_tab(self):
        """
        Method to change the current tab of the transition function
        :return:
        """
        self.tw_transitionFunctions.clear()
        if self._seperated_factors():
            self._number_of_transition_functions = 1
            self.create_transition_function('Transition function 1')
            self._number_of_transition_functions = 2
            self.create_transition_function('Transition function 2')
        else:
            self._number_of_transition_functions = 1
            self.create_transition_function('Transition function 1')

    def create_transition_function(self, tf_name: str):
        """
        Method to create a new transition dunction
        :param tf_name: name of the transition function
        """
        newTF = QtWidgets.QWidget()
        newTF.setObjectName(tf_name)
        self.tw_transitionFunctions.addTab(newTF,
                                           newTF.objectName()
                                          )
        tf_layout = QtWidgets.QVBoxLayout()
        if self._number_of_transition_functions == 1:
            tf = TransitionFunction()
            tf.set_function(""," return min(state + factor, Qmax * service_time)", 1)
        else:
            tf = TransitionFunction(2)
            tf.set_function("", " return max(state - factor, 0.0)",2)
        tf_layout.addWidget(tf)
        newTF.setLayout(tf_layout)

    def _get_service_time(self):
        """
        Method to get the service time input
        :return: service time
        """
        return float(self.le_batchSize.text())

    def _get_qmax(self):
        """
        Method to get he maximum queueing length
        :return: qmax
        """
        return int(self.le_qmax.text())

    def _service_time_adjustment(self):
        """
        Method to get the information about the service time adjustment
        :return: selection of the service time adjustment
        """
        return self.cb_serviceTimeAdjustment.isChecked()


    def _seperated_factors(self):
        """
        Method to get the information about separating the factors
        :return: selection of the factor separation
        """
        return self.cb_separateFactorDistributions.isChecked()

    def _get_transition_functions(self):
        """
        Method to get the transition function input
        :return: transition function
        """
        transition_functions = ''
        for index in range(self._number_of_transition_functions):
            self.tw_transitionFunctions.setCurrentIndex(index)
            transition_functions += self.tw_transitionFunctions.currentWidget().layout().itemAt(0) \
                .widget().get_transition_function_name()
            transition_functions += "\n    "
            lines = self.tw_transitionFunctions.currentWidget().layout().itemAt(0) \
                .widget().get_transition_function().split("\n")
            transition_functions += "\n    ".join(lines)
            transition_functions += '\n \n'
        return transition_functions

    def _set_ArrivalTime_path(self):
         """
         Methid to get the path of the file containing the arrival time distribution
         :return: path of arrival time distribution
         """
         self.le_fileInputArrivalTime.setText(QFileDialog.getOpenFileName(None, 'Open file',
                                           './resources/configuration_files/', "*.json")[0])

    def _set_BatchSize_path(self):
         """
         Method to get the path of the file containing the batch size distribution
         :return: path of batch size distribution
         """
         self.le_fileInputBatchSize.setText(QFileDialog.getOpenFileName(None, 'Open file',
                                                                         './resources/configuration_files/', "*.json")[
                                                 0])
    def visualize_distributions(self, arrival_time_distribution, batch_size_distribution):
        """
        Method for visualizing the distributions
        :param arrival_time_distribution: distribution of the arrival time
        :param batch_size_distribution: distribution of the batch size
        :return:
        """
        self.wid_arrivalTimeDistributionFunction.layout().removeWidget(self.canvas_arrivalTime)
        self.wid_batchSizeDistributionFunction.layout().removeWidget(self.canvas_batchSize)

        self.canvas_arrivalTime = FigureCanvas(arrival_time_distribution)
        self.canvas_batchSize = FigureCanvas(batch_size_distribution)


        self.wid_arrivalTimeDistributionFunction.layout().addWidget(self.canvas_arrivalTime)
        self.wid_batchSizeDistributionFunction.layout().addWidget(self.canvas_batchSize)
        self.hl_toolbarArrival.removeWidget(self.toolbar_arrivalTime)
        self.toolbar_arrivalTime = NavigationToolbar(self.canvas_arrivalTime, self)
        self.hl_toolbarArrival.addWidget(self.toolbar_arrivalTime)
        self.hl_toolbarBatch.removeWidget(self.toolbar_batchSize)
        self.toolbar_batchSize = NavigationToolbar(self.canvas_batchSize, self)
        self.hl_toolbarBatch.addWidget(self.toolbar_batchSize)

    def _generate_empty_figure(self, x_label, y_label):
        """
        Method to get a  labeled empty figure
        :param x_label: label of the x-axis
        :param y_label: label of the y-axis
        :return:
        """
        figure = plt.figure()
        plt.ylabel(x_label)
        plt.xlabel(y_label)
        plt.title('Discretized distribution')
        return figure

    def _reset(self):
        """
        Method to reset the window
        """
        self._reset_arrivalTime()
        self._reset_batchSize()
        self._disable_arrivalTime()
        self._disable_batchSize()


    def _disable_arrivalTime(self):
        """
        Method to disable the widgets associated with the arrival time
        """
        self.la_inputValuesArrivalTime.setEnabled(False)
        self.le_inputValuesArrivalTime.setEnabled(False)
        self.le_probabiliesArrivalTime.setEnabled(False)
        self.la_probabilitiesArrivalTime.setEnabled(False)

    def _disable_batchSize(self):
        """
        Method to disable the widgets associated with the batch size
        """
        self.la_inputValuesBatchSize.setEnabled(False)
        self.le_inputValuesBatchSize.setEnabled(False)
        self.le_probabiliesBatchSize.setEnabled(False)
        self.la_probabilitiesBatchSize.setEnabled(False)

    def _set_conditional_visualization(self):
        """
        method to enable a conditional visualization of the widgets of the GUI
        """
        self._reset()
        arrival_time_distribution = self.cob_arrivalTimeDistribution.currentText()


        if self.cb_maximumArrivalTime.isChecked():
            self.le_maximumArrivalTime.setEnabled(True)
        else:
            self.le_maximumArrivalTime.setText("None")

        if self.cb_maximumBatchSize.isChecked():
            self.le_maximumBatchSize.setEnabled(True)
        else:
            self.le_maximumBatchSize.setText("None")

        if arrival_time_distribution == "Exponential distribution":
            self.cb_maximumArrivalTime.setVisible(True)
            self.le_maximumArrivalTime.setVisible(True)
            self.la_rateArrivalTime.setVisible(True)
            self.le_rateArrivalTime.setVisible(True)

        elif arrival_time_distribution == "K-Erlang distribution":
            self.cb_maximumArrivalTime.setVisible(True)
            self.le_maximumArrivalTime.setVisible(True)

            self.la_rateArrivalTime.setVisible(True)
            self.la_kArrivalTime.setVisible(True)
            self.le_rateArrivalTime.setVisible(True)
            self.le_kArrivalTime.setVisible(True)

        elif arrival_time_distribution == "Hyperexponential distribution":
            self.cb_maximumArrivalTime.setVisible(True)
            self.le_maximumArrivalTime.setVisible(True)
            self.la_piArrivalTime.setVisible(True)
            self.la_liArrivalTime.setVisible(True)
            self.le_piArrivalTime.setVisible(True)
            self.le_liArrivalTime.setVisible(True)

        elif arrival_time_distribution == "Gamma distribution":
            self.cb_maximumArrivalTime.setVisible(True)
            self.le_maximumArrivalTime.setVisible(True)
            self.la_alphaArrivalTime.setVisible(True)
            self.la_betaArrivalTime.setVisible(True)
            self.le_alphaArrivalTime.setVisible(True)
            self.le_betaArrivalTime.setVisible(True)

        elif arrival_time_distribution == "Uniform distribution":
            self.la_minArrivalTime.setVisible(True)
            self.la_maxArrivalTime.setVisible(True)
            self.le_minArrivalTime.setVisible(True)
            self.le_maxArrivalTime.setVisible(True)

        elif arrival_time_distribution == "General independent distribution":
            self.rb_listInputArrivalTime.setVisible(True)
            self.la_inputValuesArrivalTime.setVisible(True)
            self.le_inputValuesArrivalTime.setVisible(True)
            self.le_probabiliesArrivalTime.setVisible(True)
            self.la_probabilitiesArrivalTime.setVisible(True)
            self.rb_fileInputArrivalTime.setVisible(True)
            self.le_fileInputArrivalTime.setVisible(True)
            self.bu_filePath_ArrivalTime.setVisible(True)

            if self.rb_listInputArrivalTime.isChecked():
                self.la_inputValuesArrivalTime.setEnabled(True)
                self.le_inputValuesArrivalTime.setEnabled(True)
                self.le_probabiliesArrivalTime.setEnabled(True)
                self.la_probabilitiesArrivalTime.setEnabled(True)

            elif self.rb_fileInputArrivalTime.isChecked():
                self.le_fileInputArrivalTime.setEnabled(True)
                self.bu_filePath_ArrivalTime.setEnabled(True)
            else:
                raise NotImplementedError

        batch_size_distribution = self.cob_batchSizeDistribution.currentText()
        if batch_size_distribution == "Exponential distribution":
            self.cb_maximumBatchSize.setVisible(True)
            self.le_maximumBatchSize.setVisible(True)
            self.la_rateBatchSize.setVisible(True)
            self.le_rateBatchSize.setVisible(True)

        elif batch_size_distribution == "K-Erlang distribution":
            self.cb_maximumBatchSize.setVisible(True)
            self.le_maximumBatchSize.setVisible(True)
            self.la_rateBatchSize.setVisible(True)
            self.la_kBatchSize.setVisible(True)
            self.le_rateBatchSize.setVisible(True)
            self.le_kBatchSize.setVisible(True)

        elif batch_size_distribution == "Hyperexponential distribution":
            self.cb_maximumBatchSize.setVisible(True)
            self.le_maximumBatchSize.setVisible(True)
            self.la_piBatchSize.setVisible(True)
            self.la_liBatchSize.setVisible(True)
            self.le_piBatchSize.setVisible(True)
            self.le_liBatchSize.setVisible(True)

        elif batch_size_distribution == "Gamma distribution":
            self.cb_maximumBatchSize.setVisible(True)
            self.le_maximumBatchSize.setVisible(True)
            self.la_alphaBatchSize.setVisible(True)
            self.la_betaBatchSize.setVisible(True)
            self.le_alphaBatchSize.setVisible(True)
            self.le_betaBatchSize.setVisible(True)

        elif batch_size_distribution == "Uniform distribution":
            self.la_minBatchSize.setVisible(True)
            self.la_maxBatchSize.setVisible(True)
            self.le_minBatchSize.setVisible(True)
            self.le_maxBatchSize.setVisible(True)

        elif batch_size_distribution == "General independent distribution":
            self.rb_listInputBatchSize.setVisible(True)
            self.la_inputValuesBatchSize.setVisible(True)
            self.le_inputValuesBatchSize.setVisible(True)
            self.le_probabiliesBatchSize.setVisible(True)
            self.la_probabilitiesBatchSize.setVisible(True)

            self.rb_fileInputBatchSize.setVisible(True)
            self.le_fileInputBatchSize.setVisible(True)
            self.bu_filePath_BatchSize.setVisible(True)

            if self.rb_listInputBatchSize.isChecked():
                self.la_inputValuesBatchSize.setEnabled(True)
                self.le_inputValuesBatchSize.setEnabled(True)
                self.le_probabiliesBatchSize.setEnabled(True)
                self.la_probabilitiesBatchSize.setEnabled(True)

            elif self.rb_fileInputBatchSize.isChecked():
                self.le_fileInputBatchSize.setEnabled(True)
                self.bu_filePath_BatchSize.setEnabled(True)
            else:
                raise NotImplementedError

    def _reset_arrivalTime(self):
        """
        Method that allows to reset the widgets associated with the arrival time
        """
        self.la_alphaArrivalTime.setVisible(False)
        self.le_alphaArrivalTime.setVisible(False)
        self.la_betaArrivalTime.setVisible(False)
        self.le_betaArrivalTime.setVisible(False)
        self.la_kArrivalTime.setVisible(False)
        self.le_kArrivalTime.setVisible(False)
        self.la_rateArrivalTime.setVisible(False)
        self.le_rateArrivalTime.setVisible(False)
        self.cb_maximumArrivalTime.setVisible(False)
        self.le_maximumArrivalTime.setVisible(False)
        self.le_maximumArrivalTime.setEnabled(False)

        self.la_minArrivalTime.setVisible(False)
        self.la_maxArrivalTime.setVisible(False)
        self.le_minArrivalTime.setVisible(False)
        self.le_maxArrivalTime.setVisible(False)


        self.la_liArrivalTime.setVisible(False)
        self.la_piArrivalTime.setVisible(False)
        self.le_liArrivalTime.setVisible(False)
        self.le_piArrivalTime.setVisible(False)


        self.rb_listInputArrivalTime.setVisible(False)
        self.la_inputValuesArrivalTime.setVisible(False)
        self.le_inputValuesArrivalTime.setVisible(False)
        self.le_probabiliesArrivalTime.setVisible(False)
        self.la_probabilitiesArrivalTime.setVisible(False)

        self.rb_fileInputArrivalTime.setVisible(False)
        self.le_fileInputArrivalTime.setVisible(False)
        self.bu_filePath_ArrivalTime.setVisible(False)
        self.bu_filePath_ArrivalTime.setEnabled(False)
        self.le_fileInputArrivalTime.setEnabled(False)



    def _reset_batchSize(self):
        """
        Method that allows to reset the widgets associated with the batch size
        """
        self.la_alphaBatchSize.setVisible(False)
        self.le_alphaBatchSize.setVisible(False)
        self.la_betaBatchSize.setVisible(False)
        self.le_betaBatchSize.setVisible(False)
        self.la_kBatchSize.setVisible(False)
        self.le_kBatchSize.setVisible(False)
        self.la_rateBatchSize.setVisible(False)
        self.le_rateBatchSize.setVisible(False)
        self.cb_maximumBatchSize.setVisible(False)
        self.le_maximumBatchSize.setVisible(False)
        self.le_maximumBatchSize.setEnabled(False)

        self.la_minBatchSize.setVisible(False)
        self.la_maxBatchSize.setVisible(False)
        self.le_minBatchSize.setVisible(False)
        self.le_maxBatchSize.setVisible(False)

        self.rb_listInputBatchSize.setVisible(False)
        self.la_inputValuesBatchSize.setVisible(False)
        self.le_inputValuesBatchSize.setVisible(False)
        self.le_probabiliesBatchSize.setVisible(False)
        self.la_probabilitiesBatchSize.setVisible(False)

        self.la_piBatchSize.setVisible(False)
        self.la_liBatchSize.setVisible(False)
        self.le_piBatchSize.setVisible(False)
        self.le_liBatchSize.setVisible(False)

        self.rb_fileInputBatchSize.setVisible(False)
        self.le_fileInputBatchSize.setVisible(False)
        self.bu_filePath_BatchSize.setVisible(False)
        self.bu_filePath_BatchSize.setEnabled(False)
        self.le_fileInputBatchSize.setEnabled(False)
