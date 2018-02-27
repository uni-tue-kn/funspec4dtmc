
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
from PyQt5 import QtGui
from FunSpec4DTMC.view.ui_strategyselectiondialog import Ui_StrategySelectionDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QFileDialog


class StrategySelectionDialog(QDialog, Ui_StrategySelectionDialog):
    strategySelected = pyqtSignal(str, int, float, int, dict, str, str, name='strategySelected')

    def __init__(self):
        """
        Constructor of the class StrategySelectionDialog
        """
        super(StrategySelectionDialog, self).__init__()

        # Set up the user interface created by the Qt Designer.
        self.current_mc_type = None
        self.setupUi(self)
        self.initialization()

    def initialization(self):
        """
        Method to initialize the graphical interface
        """
        self.setWindowIcon(QtGui.QIcon('resources/icons/FS4DTMC.png'))
        self.set_conditional_visualisation()
        self.cb_strategy.currentIndexChanged.connect(self.set_conditional_visualisation)
        self.cb_steps.clicked.connect(self.set_conditional_visualisation)
        self.cb_stStVector.clicked.connect(self.set_conditional_visualisation)
        self.cb_stStVectorPlot.clicked.connect(self.set_conditional_visualisation)
        self.cb_cuStStVectorPlot.clicked.connect(self.set_conditional_visualisation)
        self.cb_coCuStStVectorPlot.clicked.connect(self.set_conditional_visualisation)
        self.cb_alphaRelaxation.clicked.connect(self.set_conditional_visualisation)
        self.cb_graph.clicked.connect(self.set_conditional_visualisation)
        self.cb_saveSSD.clicked.connect(self.set_conditional_visualisation)
        self.cb_transitionMatrix.clicked.connect(self.set_conditional_visualisation)
        self.cb_saveTM.clicked.connect(self.set_conditional_visualisation)
        self.cb_period.clicked.connect(self.set_conditional_visualisation)
        self.bu_filePath_TM.clicked.connect(self.set_TM_save_path)
        self.bu_filePath_SSD.clicked.connect(self.set_SSD_save_path)

        self.bb_acceptStrategy.accepted.connect(self.input_accepted)

    def set_current_mc_type(self, type):
        """
        Method to set the current used Markov chain type
        :param type: current type
        :return:
        """
        self.current_mc_type = type

    def input_accepted(self):
        """
        Method to confirm the selected strategies
        :return:
        """
        try:
            self.strategySelected.emit(self.get_calculation_strategy(),
                                       self.get_simulation_steps(),
                                       self.get_alpha(),
                                       self.get_specified_period(),
                                       self.get_presentation_types(),
                                       self.get_start_state(),
                                       self.get_calculation_scheme())
        except:
            print("Analysis stopped.")

    def get_calculation_strategy(self):
        """
        Method to read the selected algorithms
        :return: selected strategy
        """
        return self.cb_strategy.currentText()

    def get_simulation_steps(self):
        """
        Method to get the optional iteration steps use for calculation
        :return: simulation stepes
        """
        if self.cb_steps.isChecked():
            try:
                return int(self.te_steps.toPlainText())
            except:
                TypeError("Input for number of steps must be an integer.")
        else:
            return None

    def get_specified_period(self):
        """
        Method to get the specified period
        :return: period
        """
        if self.cb_period.isChecked():
            return int(self.te_period.toPlainText())
        else:
            return None

    def get_alpha(self):
        """
        Method to get the optional alpha value used for alpha relaxation
        :return: alpha
        """
        if self.cb_alphaRelaxation.isChecked():
            try:
                return float(self.te_alphaRelaxation.toPlainText())
            except:
                return 1.0
        else:
            return 1.0

    def get_start_state(self):
        """
        method to get the start state for simulations
        :return:  start state
        """
        return self.le_startState.text()

    def get_calculation_scheme(self):
        """
        Method to get the selected calculation scheme in case of direct calculation
        :return:
        """
        if self.cb_strategy.currentText() == "MCS - Direct approach":
            return self.cb_directScheme.currentText()
        else:
            return ""


    def get_presentation_types(self):
        """
        Method to get the selected visualization types
        :return: presentation types
        """
        plots = {
                'graph': (False, None, False),
                'period': False,
                'stationary state distribution vector':(False, False, ""),
                'stationary state distribution plot': (False, True),
                'cumulative stationary state distribution': (False, True),
                'complementary cumulative stationary state distribution': (False, True),
                'evolution of state average':  False,
                'random walk': False,
                'evolution of state probabilities': False,
                'transition matrix': (False, False, "")
            }

        if self.cb_graph.isChecked():
            plots['graph'] = (True, self.cb_graphLayout.currentText(),  self.cb_markClosures.isChecked())

        if self.cb_calculate_period.isChecked():
            plots['period'] = True

        if self.cb_stStVector.isChecked():
            plots['stationary state distribution vector'] = (True, self.cb_saveSSD.isChecked(), self.le_filePath_SSD.text())

        if self.cb_stStVectorPlot.isChecked():
            plots['stationary state distribution plot'] = (True, self.cb_stStVectorPlotSeparated.isChecked())


        if self.cb_cuStStVectorPlot.isChecked():
            plots['cumulative stationary state distribution'] = (True, self.cb_cuStStVectorPlotSeparated.isChecked())

        if self.cb_coCuStStVectorPlot.isChecked():
            plots['complementary cumulative stationary state distribution'] =\
                (True, self.cb_coCuStStVectorPlotSeparated.isChecked())

        if self.cb_randomWalk.isChecked():
            plots['random walk'] = True

        if self.cb_evoStAv.isChecked():
            plots['evolution of state average'] = True


        if self.cb_evoSt.isChecked():
            plots['evolution of state probabilities'] = True

        if self.cb_transitionMatrix.isChecked():
            plots['transition matrix'] = (True, self.cb_saveTM.isChecked(), self.le_filePath_TM.text())

        return plots

    def set_TM_save_path(self):
        """
        Method to select the file path for storage of the resulting transition matrix using a file dialog
        :return:
        """
        file_path = self.set_path()
        self.le_filePath_TM.setText(file_path)

    def set_SSD_save_path(self):
        """
        method to set a path for storage of the resulting stationary state distribution using a file dialog
        :return: selected file path
        """
        file_path = self.set_path()
        self.le_filePath_SSD.setText(file_path)

    def set_path(self):
        """
        Method to set a path for storage of the results using a file dialog
        :return: selected file path
        """
        return str(QFileDialog.getExistingDirectory(QFileDialog(), 'Select storage path',
                                            './resources/configuration_files/'))

    def reset(self):
        """
        Method to reset the window
        """
        self.te_period.setEnabled(False)
        self.te_alphaRelaxation.setEnabled(True)
        self.cb_alphaRelaxation.setEnabled(True)
        self.cb_stStVectorPlotSeparated.setEnabled(False)
        self.cb_cuStStVectorPlotSeparated.setEnabled(False)
        self.cb_coCuStStVectorPlotSeparated.setEnabled(False)
        self.cb_markClosures.setEnabled(False)

        self.te_steps.setEnabled(False)
        self.te_alphaRelaxation.setEnabled(False)
        self.la_graphLayout.setEnabled(False)
        self.cb_graphLayout.setEnabled(False)
        self.cb_evoStAv.setVisible(False)
        self.cb_evoSt.setVisible(False)
        self.cb_randomWalk.setVisible(False)
        self.la_startState.setVisible(False)
        self.le_startState.setVisible(False)
        self.cb_alphaRelaxation.setEnabled(True)
        self.cb_steps.setEnabled(True)
        self.la_directScheme.setVisible(False)
        self.cb_directScheme.setVisible(False)
        self.cb_transitionMatrix.setVisible(False)

        self.cb_saveSSD.setEnabled(False)
        self.cb_saveTM.setEnabled(False)
        self.le_filePath_SSD.setVisible(False)
        self.le_filePath_TM.setVisible(False)
        self.bu_filePath_SSD.setVisible(False)
        self.bu_filePath_TM.setVisible(False)
        self.cb_saveTM.setVisible(False)

    def set_conditional_visualisation(self):
        """
        method that enables the visualization that depends on previous inputs
        """
        self.reset()

        if self.current_mc_type == "MarkovChainConventionalApproach":
            self.cb_strategy.model().item(6).setEnabled(False)
            self.cb_transitionMatrix.setChecked(False)

        elif self.current_mc_type == "MarkovChainForwardApproach":
            self.cb_strategy.model().item(0).setEnabled(False)
            self.cb_strategy.model().item(1).setEnabled(False)
            self.cb_strategy.model().item(2).setEnabled(False)
            self.cb_strategy.model().item(3).setEnabled(False)
            self.cb_strategy.model().item(4).setEnabled(False)
            self.cb_strategy.model().item(5).setEnabled(False)
            self.cb_strategy.setCurrentIndex(6)


        if self.cb_steps.isChecked():
            self.te_steps.setEnabled(True)

        if self.cb_period.isChecked():
            self.te_period.setEnabled(True)

        if self.cb_alphaRelaxation.isChecked():
            self.te_alphaRelaxation.setEnabled(True)

        if self.cb_graph.isChecked():
            self.cb_markClosures.setEnabled(True)
            self.la_graphLayout.setEnabled(True)
            self.cb_graphLayout.setEnabled(True)

        if self.cb_strategy.currentText() == "MCS - Forward approach":
            self.cb_transitionMatrix.setVisible(True)
            self.cb_saveTM.setVisible(True)
            if self.cb_transitionMatrix.isChecked():
                self.cb_saveTM.setEnabled(True)
                if self.cb_saveTM.isChecked():
                    self.le_filePath_TM.setVisible(True)
                    self.bu_filePath_TM.setVisible(True)

        elif self.cb_strategy.currentText() == "MCS - Random walk":
            self.cb_evoStAv.setVisible(True)
            self.cb_randomWalk.setVisible(True)
            self.cb_evoSt.setVisible(True)
            self.la_startState.setVisible(True)
            self.le_startState.setVisible(True)
            self.cb_alphaRelaxation.setEnabled(False)
            self.te_alphaRelaxation.setEnabled(False)

        elif self.cb_strategy.currentText() == "MCS - Direct approach":
            self.cb_alphaRelaxation.setEnabled(False)
            self.cb_steps.setEnabled(False)
            self.la_directScheme.setVisible(True)
            self.cb_directScheme.setVisible(True)

        if not self.cb_strategy.currentText() == "MCS - Random walk":
            self.cb_randomWalk.setChecked(False)
            self.cb_evoSt.setChecked(False)
            self.cb_evoStAv.setChecked(False)
        if self.cb_stStVector.isChecked():
            self.cb_saveSSD.setEnabled(True)
            if self.cb_saveSSD.isChecked():
                self.le_filePath_SSD.setVisible(True)
                self.bu_filePath_SSD.setVisible(True)

        if self.cb_stStVectorPlot.isChecked():
            self.cb_stStVectorPlotSeparated.setEnabled(True)

        if self.cb_cuStStVectorPlot.isChecked():
            self.cb_cuStStVectorPlotSeparated.setEnabled(True)

        if self.cb_coCuStStVectorPlot.isChecked():
            self.cb_coCuStStVectorPlotSeparated.setEnabled(True)

