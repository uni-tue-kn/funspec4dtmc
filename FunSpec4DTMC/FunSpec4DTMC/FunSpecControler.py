
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

from FunSpec4DTMC.view.mainwindow import MainWindow
from FunSpec4DTMC.model.SimulationControler import SimulationControler
from FunSpec4DTMC.model.parser.FunSpecParser import FunSpecParser
import multiprocessing
from multiprocessing import Process, Manager
import time


class Simulator:

    def __init__(self):
        """
        Constructor of the class Simulator
        """
        self.fs_view = MainWindow()
        self._number_of_projects = 0
        self._project_number = 1
        self.projects = []
        self.new_project()
        self.persistence = False
        self.ignore_input_visualisation = False
        self.fs_parser = FunSpecParser()
        self.initialize()


    def initialize(self):
        """
        Method that initializes the simulator and thus the GUI and the model.
        """
        self.fs_view.start_gui()
        self.initialize_mode()
        self.bind_signals()
        self.select_project()

    def bind_signals(self):
        """
        Function handles the binding of signals from the graphical user interface to functions of the simulator
        """
        self.fs_view.projectChanged.connect(self.change_project)
        self.fs_view.systemVisualizationTriggered.connect(self.system_input_visualization)
        self.fs_view.systemInputProcessingTriggered.connect(self.system_input_processing)
        self.fs_view.mcInputConfirmed.connect(self.add_markov_chain)
        self.fs_view.strategySelected.connect(self.select_calculation_method)
        self.fs_view.saveDialogOpened.connect(self.save_mc)
        self.fs_view.modeSelected.connect(self.change_mode)
        self.fs_view.calculationPrecisionAdjusted.connect(self.adjust_calculation_precision)
        self.fs_view.displayPrecisionAdjusted.connect(self.adjust_display_precision)
        self.fs_view.discretizationPrecisionAdjusted.connect(self.adjust_dicretization_precision)
        self.fs_view.persistenceSet.connect(self.set_persistence)
        self.fs_view.ignoreInputVisualization.connect(self.set_input_visualisation_ignored)

    def initialize_mode(self):
        """
        Method for initializing, checking and activating the Cython mode
        """
        try:
            import cython
        except ModuleNotFoundError:
            self.fs_view.enableCythonMode(False)
            self.simulation_simulator.enableCythonMode(False)

    def change_mode(self, cython_mode: bool, research_mode: bool):
        """
        Method which allows the mode switching.
        :param cython_mode: Selected if Cython module enables
        :param research_mode: Selected if research module enables
        """
        self.enable_cython_mode(cython_mode)
        self.enable_research_mode(research_mode)


    def enable_cython_mode(self, cython_mode: bool):
        """
        Method that enables activation of the cython modes
        :param  cython_mode: Selected if Cython module enables
        """
        self.simulation_simulator.enableCythonMode(cython_mode)

    def enable_research_mode(self, research_mode: bool):
        """
        Method that enables activation of the research modes
        :param research_mode: Selected if research module enables
        """
        self.simulation_simulator.enableResearchMode(research_mode)

    def set_input_visualisation_ignored(self, ignored: bool):
        """
        Method that allows you to suppress input visualization
        :param ignored: Selected if input visualization is suppressed
        """
        self.ignore_input_visualisation = ignored

    def adjust_calculation_precision(self, precision: float):
        """
        Method for adjusting the accuracy of calculation of the simulator
        :param precision: Chosen accuracy
        """
        self.simulation_simulator.adjust_precision(precision)

    def adjust_dicretization_precision(self, precision: float):
        """
        Method for adjusting the accuracy of discretization of continuous distributions
        :param precision: Chosen accuracy
        """
        self.simulation_simulator.adjust_discretization_precision(precision)

    def adjust_display_precision(self, precision: float):
        """
        Method for adjusting the display accuracy of the GUI
        :param precision: Chosen accuracy
        """
        self.fs_parser.set_display_precision(precision)

    def set_persistence(self, persistence: bool):
        """
        Method for adapting the persistence of plots in the graphical interface
        :param persistence: Selected if the plots should remain visualized when recalculating them.
        """
        self.persistence = persistence

    def update_calculation_characteristics(self, steps: int, norm: float):
        """
        Function for updating the calculation characteristics in the graphical user interface
        :param steps: Current iteration step of the calculation
        :param norm: Current Ddviation of the state vector from the previous one in norm
        """
        try:
            self.fs_view.update_calculation_characteristics(steps, norm)
        except:
            raise InterruptedError

    def new_project(self):
        """
        Method for generating a new project
        """
        self._number_of_projects += 1
        self.simulation_simulator = SimulationControler()
        self.simulation_simulator.set_calculation_listener(self.update_calculation_characteristics)
        self.projects.append(self.simulation_simulator)
        if self._number_of_projects > 1:
            self.fs_view.new_project()


    def change_project(self, project_number: int):
        """
        Method for changing the current new project
        :param project_number: nu
        """
        self._project_number = project_number + 1
        if self._project_number == self._number_of_projects + 1:
            self.new_project()
        else:
            self.select_project()
            markov_chains = self.simulation_simulator.get_markov_chains()
            if markov_chains:
                self.set_current_mc_type(markov_chains[0].get_type())
            else:
                self.set_current_mc_type(None)


    def select_project(self):
        """
        Number of the project to be selected
        """
        self.simulation_simulator = self.projects[self._project_number - 1]
        self.fs_view.set_current_project(self._project_number - 1)


    def system_input_visualization(self, system_type: str, system_input: dict, service_time_adjustment: bool):
        """
        Function for and visualization of the system input
        :param system_type:
        :param system_input: configuration input of the system
        :param service_time_adjustment: Selected if a service time adjustment of the service time to calculation
        accuracy is desired.
        """
        system_configuration = self.fs_parser.get_system_configuration(system_input)
        if system_type == "GI^GI/D/1-Qmax":
            system = self.simulation_simulator.set_queueing_system(system_configuration)
        else:
            raise NotImplementedError
        system.get_distribution_function_plots(service_time_adjustment)
        self.fs_view.visualize_distributions(*system.get_distribution_function_plots(service_time_adjustment))


    def system_input_processing(self, system_type: str, system_input: dict, service_time_adjustment: bool, separated_factors: bool):
        """
        Function for and visualization of the system input
        :param system_type:
        :param system_input: configuration input of the system
        :param service_time_adjustment: Selected if a service time adjustment of the service time to calculation
        accuracy is desired.
        :param separated_factors: Selected if the factors should be stored separately
        """
        system_configuration = self.fs_parser.get_system_configuration(system_input)
        if system_type == "GI^GI/D/1-Qmax":
            system = self.simulation_simulator.set_queueing_system(system_configuration)
        else:
            raise NotImplementedError
        markov_chain_input = system.calculate_mc_specification(service_time_adjustment, separated_factors)
        self.visualize_mc_from_system(markov_chain_input)


    def visualize_mc_from_system(self, markov_chain_input: dict):
        """
        Function that visualizes the Markov chains created by system input.
        :param markov_chain_input: Markov chain input to be displayed
        """
        file_path = './resources/configuration_files/system_generated_mc.json'
        if len(markov_chain_input[0]) > 3 or len(markov_chain_input[3]) > 3 or len(markov_chain_input[0][0]) > 100 or len(markov_chain_input[3][0]) > 100:
            self.fs_parser.save_functional_mc_input(markov_chain_input, file_path)
            self.fs_view.set_mc_spezification("Number of get_states exeeds limit.", "Number of get_states exeeds limit.",
                                           "Number of get_states exeeds limit.", "Number of factors exeeds limit.",
                                           "Number of factors exeeds limit.", "", file_path)
        else:
            self.fs_view.set_mc_spezification(markov_chain_input[0], markov_chain_input[1], markov_chain_input[2],
                                              markov_chain_input[3], markov_chain_input[4], markov_chain_input[5],
                                              None)

    def add_markov_chain(self, mc_type: str, mc_configuration: dict, outsourced_definition: bool):
        """
        Function to add a Markov chain.
        :param mc_type: type of the Markov chain. Either MarkovChainForwardApproach or MarkovChainConventionalApproach
        :param mc_configuration: configuration date of the Markov chain
        :param outsourced_definition: Specifies an input type. Selection between file and GUI input.
        :return:
        """
        if mc_type == "conventional":

            if outsourced_definition:

                input_file_path = self.fs_view.get_input_file_path()
                try:
                    (initial_state_vector,
                     transition_matrix,
                     state_designations) = self.fs_parser.parse_conventional_input(input_file_path=input_file_path)

                except Exception:
                    self.fs_view.show_input_file_error_dialog()
                    return
                self.set_current_mc_type("MarkovChainConventionalApproach")

            else:
                try:
                    (initial_state_vector, transition_matrix, state_designations) = \
                        self.fs_parser.parse_conventional_input(configuration=mc_configuration)
                except Exception:
                    self.fs_view.show_input_error_dialog()
                    return
                self.set_current_mc_type("MarkovChainConventionalApproach")

            self.simulation_simulator.add_conventional_markov_chain(initial_state_vector, transition_matrix, state_designations)

        elif mc_type == 'forward':
            if outsourced_definition:
                input_file_path = self.fs_view.get_input_file_path()
                try:
                    (states,
                     state_space_names,
                     state_designations,
                     initial_state_vector,
                     factors,
                     factor_state_names,
                     factor_distribution,
                     transition_functions) = self.fs_parser.parse_forward_input(input_file_path=input_file_path,
                                                                                num_project=self._project_number,
                                                                                num_mc=self.simulation_simulator.get_number_of_mc() + 1)

                except Exception:
                    self.fs_view.show_input_file_error_dialog()
                    return

                self.set_current_mc_type("MarkovChainForwardApproach")
            else:
                try:
                    (states,
                     state_space_names,
                     state_designations,
                     initial_state_vector,
                     factors,
                     factor_state_names,
                     factor_distribution,
                     transition_functions) = self.fs_parser.parse_forward_input(configuration=mc_configuration,
                                                                                num_project=self._project_number,
                                                                                num_mc=self.simulation_simulator.get_number_of_mc() + 1)
                except Exception:
                    self.fs_view.show_input_error_dialog()
                    return

                self.set_current_mc_type("MarkovChainForwardApproach")
            self.simulation_simulator.add_forward_markov_chain(states, state_space_names, initial_state_vector,
                                                               factors, factor_state_names, factor_distribution, transition_functions)
        else:
            raise NotImplementedError('This definition is not supported')

        if not self.ignore_input_visualisation:
            try:
                manager = Manager()
                results = manager.list([])
                p = multiprocessing.Process(target=self.fs_parser.get_mc_visualisations,
                                            args=(self.simulation_simulator.get_markov_chains(), results,
                                                  self._project_number, self.simulation_simulator.get_number_of_mc()))

                p.start()
                termination_information = (False, False)
                while True:
                    timeout(p)
                    if not p.is_alive():
                        break
                    if not termination_information[1]:
                        termination_information = self.fs_view.input_visualization_aborted()
                        if termination_information[0]:
                            break
                p.terminate()
                self.fs_view.clear_input()
                self.fs_view.visualize_input(results)
            except:
                print("fehler")
        self.enable_simulation()
        self.enable_saving()





    def set_current_mc_type(self, type: str):
        """
        Function to set the current Markov chain type
        :param type: type of the Markov chain. Either MarkovChainForwardApproach of MarkovChainConventionalApproach
        """
        self.fs_view.set_current_mc_type(type)

    def enable_saving(self):
        """
        Function that allows saving markov chains
        """
        self.fs_view.enable_saving()

    def save_mc(self, filePath: bool, num_markov_chain: int):
        """
        Function that starts saving the markov chain
        :param filePath: path of the storage file
        :param num_markov_chain: number of the current Markov chain
        :return:
        """
        markov_chain = self.simulation_simulator.get_markov_chains()[num_markov_chain]

        if markov_chain.get_type() == 'MarkovChainConventionalApproach':
            self.fs_parser.save_conventional_mc(markov_chain, filePath)
        elif markov_chain.get_type() == 'MarkovChainForwardApproach':
            self.fs_parser.save_functional_mc(markov_chain, filePath)
        else:
            pass


    def enable_simulation(self):
        """
        Function that allows unlocking the simulation functionality in the view
        """
        self.fs_view.enable_simulation()


    def select_calculation_method(self, calculation_method: str, steps: int, alpha: float, specified_period: int,
                                  visualisation_types: dict, start_state: int=0, scheme: str=None):
        """
        Function that allows the selection of the calculation algorithms
        :param calculation_method: method that has been requested
        :param steps: Number of iteration steps at creation
        :param alpha: value needed for alpha-relaxation
        :param visualisation_types: plots that have been requested
        :param start_state: a start state for MC simulation
        :param scheme: calculation schemes in the case of the direct approach
        :return:
        """
        if calculation_method == 'MCS - Matrix powering':
            self.simulation_simulator.instantiate_MCSMatrixPowering()

        elif calculation_method == 'MCS - Random walk':
            self.simulation_simulator.instantiate_MCSRandomWalk(start_state)

        elif calculation_method == 'MCS - Cesaro limit':
            self.simulation_simulator.instantiate_MCSCesaroLimit()

        elif calculation_method == 'MCS - Modified cesaro limit':
            self.simulation_simulator.instantiate_MCSModifiedCesaroLimit()

        elif calculation_method == 'MCS - Limiting distribution':
            self.simulation_simulator.instantiate_MCSLimitingDistribution()

        elif calculation_method == 'MCS - Direct approach':
            self.simulation_simulator.instantiate_MCSDirectApproach(scheme)

        elif calculation_method == 'MCS - Forward approach':
            self.simulation_simulator.instantiate_MCSForwardApproach()


        else:
            raise NotImplementedError('This simulation method is not implemented')
        try:
            self.visualize_results(visualisation_types, steps, alpha, specified_period)
        except:
            pass

    def visualize_results(self, plot: dict, steps: int, alpha: float, specified_period):
        """
        Function for selection and controlling creation visualization of the results
        :param plot: Plots that have been requested
        :param steps: Number of iteration steps at creation
        :param alpha: value needed for alpha-relaxation
        :param specified_period: specified value for period
        """
        if self.persistence is False:
            self.fs_view.clear_results()

        graph_plot = plot['graph']
        if graph_plot[0]:

            figures, titles = self.simulation_simulator.get_graph_plot(graph_plot[1], graph_plot[2])
            for index in range(len(figures)):
                self.fs_view.visualize_results(figures[index], "Graph of {mc}".format(mc=titles[index]))

        if plot['period']:
            periods, titles = self.simulation_simulator.calculate_period()
            for index in range(len(periods)):
                self.fs_view.visualize_results(self.fs_parser.plot_period(periods[index]),
                                            "Period of {mc}".format(mc=titles[index]))

        ssd_vector = plot["stationary state distribution vector"]
        if ssd_vector[0]:
            try:
                stationary_state_distributions, titles = self.simulation_simulator.calculate_stationary_state_distributions(steps, alpha, specified_period)
                for index in range(len(stationary_state_distributions)):
                    self.fs_view.visualize_results(self.fs_parser.vector_plot(stationary_state_distributions[index]),
                                                "Stationary state distribution vector of {mc}".format(mc=titles[index]))
                    if ssd_vector[1]:
                        path = ssd_vector[2] + '/stationary_state_distribution_mc{mc}.json'.format(mc=index)
                        self.fs_parser.save_vector(stationary_state_distributions[index], path)
            except:
                self.fs_view.show_calculation_error_dialog()
                raise InterruptedError


        ssd_plot = plot['stationary state distribution plot']
        if ssd_plot[0]:
            try:
                figures, titles = self.simulation_simulator.plot_stationary_state_distributions(steps,
                                                                                                alpha,
                                                                                                specified_period,
                                                                                                ssd_plot[1])
                for index in range(len(figures)):
                    self.fs_view.visualize_results(figures[index], "SSD plot of {mc}".format(mc=titles[index]))
            except:
                self.fs_view.show_calculation_error_dialog()
                raise InterruptedError

        cssd_plot = plot["cumulative stationary state distribution"]
        if cssd_plot[0]:
            try:
                figures, titles = self.simulation_simulator.plot_cumulative_stationary_state_distributions(steps,
                                                                                                           alpha,
                                                                                                           specified_period,
                                                                                                           cssd_plot[1])
                for index in range(len(figures)):
                    self.fs_view.visualize_results(figures[index], "CSSD plot of {mc}".format(mc=titles[index]))
            except:
                self.fs_view.show_calculation_error_dialog()
                raise InterruptedError

        ccssd_plot = plot["complementary cumulative stationary state distribution"]
        if ccssd_plot[0]:
            try:
                figures, titles = self.simulation_simulator.plot_complementary_cumulative_stationary_state_distributions(steps,
                                                                                                                         alpha,
                                                                                                                         specified_period,
                                                                                                                         ccssd_plot[1])
                for index in range(len(figures)):
                    self.fs_view.visualize_results(figures[index], "Complementary CSSD plot of {mc}".format(mc=titles[index]))
            except:
                self.fs_view.show_calculation_error_dialog()
                raise InterruptedError

        if plot["evolution of state average"]:
            try:
                figures, titles = self.simulation_simulator.plot_evolution_of_state_average(steps)
                for index in range(len(figures)):
                    self.fs_view.visualize_results(figures[index], "Evolution of state average plot of {mc}".format(mc=titles[index]))
            except:
                self.fs_view.show_calculation_error_dialog()
                raise InterruptedError

        if plot["random walk"]:
            try:
                figures, titles = self.simulation_simulator.plot_random_walk(steps)
                for index in range(len(figures)):
                    self.fs_view.visualize_results(figures[index], "Random walk plot of {mc}".format(mc=titles[index]))
            except:
                self.fs_view.show_calculation_error_dialog()
                raise InterruptedError

        if plot["evolution of state probabilities"]:
            try:
                figures, titles = self.simulation_simulator.plot_evolution_of_state_probabilities(steps)
                for index in range(len(figures)):
                    self.fs_view.visualize_results(figures[index], "Evolution of state probabilities plot of {mc}".format(mc=titles[index]))
            except:
                self.fs_view.show_calculation_error_dialog()
                raise InterruptedError

        vector_tm = plot["transition matrix"]
        if vector_tm[0]:
            try:
                transition_matrices, titles = self.simulation_simulator.get_transition_matrix()
                for index in range(len(transition_matrices)):

                    self.fs_view.visualize_results(self.fs_parser.matrix_plot(transition_matrices[index]),
                                                "Transition matrix of {mc}".format(mc=titles[index]))
                    if vector_tm[1]:
                        path = vector_tm[2] + '/transition_matrix_mc{mc}.json'.format(mc=index)
                        self.fs_parser.save_matrix(transition_matrices[index], path)
            except:
                self.fs_view.show_calculation_error_dialog()
                raise InterruptedError

def timeout(process):
    """
    Method that allows to raise a timeout error after a number of seconds
    """
    for i in range(30):
        if process.is_alive():
            time.sleep(1)
