
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


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(1077, 701)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonTextOnly)
        self.qwidgetMainWindow = QtWidgets.QWidget(MainWindow)
        self.qwidgetMainWindow.setObjectName("qwidgetMainWindow")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.qwidgetMainWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidgetMainWindow = QtWidgets.QTabWidget(self.qwidgetMainWindow)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidgetMainWindow.setFont(font)
        self.tabWidgetMainWindow.setObjectName("tabWidgetMainWindow")
        self.horizontalLayout.addWidget(self.tabWidgetMainWindow)
        MainWindow.setCentralWidget(self.qwidgetMainWindow)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1077, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuSettings = QtWidgets.QMenu(self.menuBar)
        self.menuSettings.setObjectName("menuSettings")
        self.menuMode = QtWidgets.QMenu(self.menuSettings)
        self.menuMode.setObjectName("menuMode")
        self.menuApplication_area = QtWidgets.QMenu(self.menuSettings)
        self.menuApplication_area.setObjectName("menuApplication_area")
        self.menuSave = QtWidgets.QMenu(self.menuBar)
        self.menuSave.setObjectName("menuSave")
        self.menuPrecision = QtWidgets.QMenu(self.menuBar)
        self.menuPrecision.setObjectName("menuPrecision")
        self.menuDisplay_settings = QtWidgets.QMenu(self.menuBar)
        self.menuDisplay_settings.setObjectName("menuDisplay_settings")
        self.menuSet_persistence_of_results = QtWidgets.QMenu(self.menuDisplay_settings)
        self.menuSet_persistence_of_results.setObjectName("menuSet_persistence_of_results")
        self.menuIgnore_input_visualization = QtWidgets.QMenu(self.menuDisplay_settings)
        self.menuIgnore_input_visualization.setObjectName("menuIgnore_input_visualization")
        MainWindow.setMenuBar(self.menuBar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setCheckable(False)
        self.actionSave.setEnabled(False)
        self.actionSave.setObjectName("actionSave")
        self.actionPythonMode = QtWidgets.QAction(MainWindow)
        self.actionPythonMode.setCheckable(True)
        self.actionPythonMode.setChecked(True)
        self.actionPythonMode.setObjectName("actionPythonMode")
        self.actionCythonMode = QtWidgets.QAction(MainWindow)
        self.actionCythonMode.setCheckable(True)
        self.actionCythonMode.setObjectName("actionCythonMode")
        self.actionSet_calculation_precision = QtWidgets.QAction(MainWindow)
        self.actionSet_calculation_precision.setObjectName("actionSet_calculation_precision")
        self.actionResearchUsage = QtWidgets.QAction(MainWindow)
        self.actionResearchUsage.setCheckable(True)
        self.actionResearchUsage.setChecked(True)
        self.actionResearchUsage.setObjectName("actionResearchUsage")
        self.actionTeachingUsage = QtWidgets.QAction(MainWindow)
        self.actionTeachingUsage.setCheckable(True)
        self.actionTeachingUsage.setObjectName("actionTeachingUsage")
        self.actionSet_display_accuracy = QtWidgets.QAction(MainWindow)
        self.actionSet_display_accuracy.setCheckable(False)
        self.actionSet_display_accuracy.setObjectName("actionSet_display_accuracy")
        self.actionDisplay_plots_of_previous_simulations = QtWidgets.QAction(MainWindow)
        self.actionDisplay_plots_of_previous_simulations.setCheckable(True)
        self.actionDisplay_plots_of_previous_simulations.setObjectName("actionDisplay_plots_of_previous_simulations")
        self.actionDiscard_plots_of_past_simulations = QtWidgets.QAction(MainWindow)
        self.actionDiscard_plots_of_past_simulations.setCheckable(True)
        self.actionDiscard_plots_of_past_simulations.setChecked(True)
        self.actionDiscard_plots_of_past_simulations.setObjectName("actionDiscard_plots_of_past_simulations")
        self.actionTrue = QtWidgets.QAction(MainWindow)
        self.actionTrue.setCheckable(True)
        self.actionTrue.setChecked(False)
        self.actionTrue.setObjectName("actionTrue")
        self.actionFalse = QtWidgets.QAction(MainWindow)
        self.actionFalse.setCheckable(True)
        self.actionFalse.setChecked(True)
        self.actionFalse.setObjectName("actionFalse")
        self.actionSet_discretization_precision = QtWidgets.QAction(MainWindow)
        self.actionSet_discretization_precision.setObjectName("actionSet_discretization_precision")
        self.menuMode.addSeparator()
        self.menuMode.addAction(self.actionPythonMode)
        self.menuMode.addAction(self.actionCythonMode)
        self.menuMode.addSeparator()
        self.menuApplication_area.addAction(self.actionResearchUsage)
        self.menuApplication_area.addAction(self.actionTeachingUsage)
        self.menuSettings.addAction(self.menuMode.menuAction())
        self.menuSettings.addAction(self.menuApplication_area.menuAction())
        self.menuSave.addAction(self.actionSave)
        self.menuPrecision.addAction(self.actionSet_calculation_precision)
        self.menuPrecision.addAction(self.actionSet_discretization_precision)
        self.menuSet_persistence_of_results.addAction(self.actionDisplay_plots_of_previous_simulations)
        self.menuSet_persistence_of_results.addAction(self.actionDiscard_plots_of_past_simulations)
        self.menuIgnore_input_visualization.addSeparator()
        self.menuIgnore_input_visualization.addAction(self.actionTrue)
        self.menuIgnore_input_visualization.addAction(self.actionFalse)
        self.menuDisplay_settings.addAction(self.actionSet_display_accuracy)
        self.menuDisplay_settings.addAction(self.menuSet_persistence_of_results.menuAction())
        self.menuDisplay_settings.addAction(self.menuIgnore_input_visualization.menuAction())
        self.menuBar.addAction(self.menuSettings.menuAction())
        self.menuBar.addAction(self.menuPrecision.menuAction())
        self.menuBar.addAction(self.menuDisplay_settings.menuAction())
        self.menuBar.addAction(self.menuSave.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidgetMainWindow.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FunSpec4DTMC"))
        self.menuSettings.setTitle(_translate("MainWindow", "Mode settings"))
        self.menuMode.setTitle(_translate("MainWindow", "Calculation mode"))
        self.menuApplication_area.setTitle(_translate("MainWindow", "Application area"))
        self.menuSave.setTitle(_translate("MainWindow", "Save Markov chain"))
        self.menuPrecision.setTitle(_translate("MainWindow", "Calculation settings"))
        self.menuDisplay_settings.setTitle(_translate("MainWindow", "Display settings"))
        self.menuSet_persistence_of_results.setTitle(_translate("MainWindow", "Set persistence of results"))
        self.menuIgnore_input_visualization.setTitle(_translate("MainWindow", "Ignore input visualization"))
        self.actionSave.setText(_translate("MainWindow", "Save Markov chain"))
        self.actionPythonMode.setText(_translate("MainWindow", "Python mode"))
        self.actionCythonMode.setText(_translate("MainWindow", "Cython mode"))
        self.actionSet_calculation_precision.setText(_translate("MainWindow", "Set calculation precision"))
        self.actionResearchUsage.setText(_translate("MainWindow", "Usage in research"))
        self.actionTeachingUsage.setText(_translate("MainWindow", "Usage in teaching"))
        self.actionSet_display_accuracy.setText(_translate("MainWindow", "Set display accuracy"))
        self.actionDisplay_plots_of_previous_simulations.setText(_translate("MainWindow", "Display plots of previous simulations"))
        self.actionDiscard_plots_of_past_simulations.setText(_translate("MainWindow", "Discard plots of previous simulations"))
        self.actionTrue.setText(_translate("MainWindow", "True"))
        self.actionFalse.setText(_translate("MainWindow", "False"))
        self.actionSet_discretization_precision.setText(_translate("MainWindow", "Set discretization precision"))

