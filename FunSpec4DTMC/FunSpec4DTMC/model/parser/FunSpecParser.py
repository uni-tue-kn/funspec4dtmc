
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

import json
import os
import os.path
import re
import os.path
import matplotlib.pyplot as plt
import numpy as np
import subprocess
plt.rc('text', usetex=True)


class FunSpecParser:
    def __init__(self):
        """
        Constructor of the class Parser
        """
        self._configuration_file = ""
        self._configuration_data = {}
        self.num_fun = 1
        self.num_mc = 1
        self.num_project = 1
        self.display_precision = 2

    def set_display_precision(self, precision):
        """
        Function to adjust the display accuracy
        :param precision: Accuracy to be used for visualization
        """
        self.display_precision = precision

########################################################################################################################
#                                                                                                                      #
#                                             Parse conventional input                                                 #
#                                                                                                                      #
########################################################################################################################

    def parse_conventional_input(self, configuration=None,
                                 input_file_path=None,
                                 output_file_path=None
                                 ):
        """
        Function for parsing Markov chains in the conventional specification
        :param configuration: Input configuration of the Markov chain
        :param input_file_path: external input file path
        :param output_file_path: external file path for swapping mechanism
        :return:
        """

        if output_file_path is None:
            output_file_path = "./resources/outsourced_calculation/"
        try:
            if configuration is not None:
                self._configuration_data = configuration
            elif input_file_path is not None:
                self._load_configuration(input_file_path)
            else:
                raise NotImplementedError
        except:
            raise MemoryError
        try:
            state_designations = self._get_state_designation()
        except:
            state_designations = self._get_state_designation(output_file_path)
        try:
            initial_state_vector = self._get_initial_state_vector()
        except:
            initial_state_vector = self._get_initial_state_vector(output_file_path)
        transition_matrix_dimension = len(initial_state_vector)
        try:
            transition_matrix = self._get_transition_matrix(transition_matrix_dimension)
        except:
            transition_matrix = self._get_transition_matrix(transition_matrix_dimension, output_file_path)
        return initial_state_vector, transition_matrix, state_designations

    def _load_configuration(self, path):
        """
        Function that reads the JSON data
        :param path: input file path
        :return:
        """
        try:
            self._configuration_file = path
            with open(path, 'r') as config:
                self._configuration_data = json.load(config)
                config.close()
        except:
            raise MemoryError

    def _get_states(self):
        """
        Function that allows to read the state space input
        :return: array of states
        """
        states = self._configuration_data["States"]
        if isinstance(states, range):
            return states

        elif type(states) is list:
            return np.array(states)
        elif isinstance(states, str):
            return np.array(states.split(","), dtype=int)
        else:
            raise NotImplementedError

    def _get_state_designation(self, output_file_path=None) -> list or None:
        """
        Function that allows to read the state designation input
        :param output_file_path: external file path for swapping mechanism
        :return: list of state designations
        """
        try:
            if output_file_path is None:
                state_designation = self._configuration_data["State designations"]
                if type(state_designation) is list:
                    if len(state_designation) == 1:
                        return state_designation[0].split(",")
                    else:
                        return state_designation
                elif state_designation is None:
                    return None
                else:
                    raise NotImplementedError
            else:
                state_designation = ""
                input = ""
                with open(self._configuration_file) as config:
                    i = 0
                    while True:

                        i += 1

                        c = config.read(1)
                        if c != "":
                            i = 0
                        if i >= 20000:
                            raise IOError
                        if c == "\"" or c == "\'":
                            while True:
                                c = config.read(1)
                                if c == "\"" or c == "\'":
                                    c += " "
                                    break
                                else:
                                    input += c
                        if input == 'State designations':
                            while True:
                                c = config.read(1)
                                if c == "N" or c == "n":
                                    return None
                                if c == "[":
                                    while True:
                                        c = config.read(1)
                                        if c == "]":
                                            state_designation = state_designation.split(",")
                                            state_designation = [str(v).replace("\"", " ").replace("\'", " ") for v in state_designation]
                                            designations = np.memmap(self.get_memmap_path(output_file_path) , dtype="S10",
                                                                             mode='w+',
                                                                             shape=len(state_designation))
                                            designations[:] = state_designation[:]
                                            del state_designation
                                            return designations
                                        else:
                                            state_designation += c
                        else:
                            input = ''
        except:
            raise IOError

    def _get_initial_state_vector(self, output_file_path=None):
        """
        Function that allows to read the initial state vector input
        :param output_file_path: external file path for swapping mechanism
        :return: array of initial state probabilities
        """
        try:
            if output_file_path is None:
                input_vector = self._configuration_data["Initial state vector"]

                if type(input_vector) is list:
                    initial_state_vector = np.array([], dtype=float)
                    for value in input_vector:
                        if isinstance(value, str):
                            value = value.split("/")
                            if len(value) == 1:
                                value = float(value[0])
                            elif len(value) == 2:
                                value = float(value[0])/float(value[1])
                            else:
                                raise TypeError
                        initial_state_vector = np.append(initial_state_vector, [value])
                    return initial_state_vector
                else:
                    raise NotImplementedError
            else:
                state_vector = ""
                input = ""
                with open(self._configuration_file) as config:
                    i = 0
                    while True:

                        i += 1

                        c = config.read(1)
                        if c != "":
                            i = 0
                        if i >= 20000:
                            raise IOError
                        if c == "\"" or c == "\'":
                            while True:
                                c = config.read(1)
                                if c == "\"" or c == "\'":
                                    c += " "
                                    break
                                else:
                                    input += c
                        if input == 'Initial state vector':
                            while True:
                                c = config.read(1)
                                if c == "[":
                                    while True:
                                        c = config.read(1)
                                        if c == "]":
                                            state_vector = state_vector.split(",")
                                            state_vector = self.cast_to_float_vector(state_vector)
                                            initial_state_vector = np.memmap(self.get_memmap_path(output_file_path), dtype=float, mode='w+',
                                                                             shape=len(state_vector))
                                            initial_state_vector[:] = state_vector[:]
                                            del state_vector
                                            return initial_state_vector
                                        else:
                                            state_vector += c
                        else:
                            input = ''
        except:
            raise IOError

    def _get_transition_matrix(self, transition_matrix_dimension, output_file_path=None):
        """
        Function that allows to read the state transition matrix input
        :param output_file_path: external file path for swapping mechanism
        :return: transition matrix
        """

        try:
            if output_file_path is None:
                if type(self._configuration_data["Transition matrix"]) is list:
                    if output_file_path is None:
                        input_matrix = self._configuration_data["Transition matrix"]
                        transition_matrix = []
                        for input_line in input_matrix:
                            line = []

                            for value in input_line:

                                if isinstance(value, str):
                                    value = value.split("/")
                                    if len(value) == 1:
                                        value = float(value[0])
                                    elif len(value) == 2:
                                        value = float(value[0]) / float(value[1])
                                    else:
                                        raise TypeError

                                line.append(value)
                            transition_matrix.append(line)
                        transition_matrix = np.array(transition_matrix, dtype=float)
                        return transition_matrix
            else:
                matrix = ""
                input = ""

                transition_matrix = np.memmap(self.get_memmap_path(output_file_path), dtype=float, mode='w+',
                                                 shape=(transition_matrix_dimension, transition_matrix_dimension))

                with open(self._configuration_file) as config:
                    i = 0
                    while True:

                        i += 1

                        c = config.read(1)
                        if c != "":
                            i = 0
                        if i >= 20000:
                            raise IOError
                        if c == "\"" or c == "\'":
                            while True:
                                c = config.read(1)
                                if c == "\"" or c == "\'":
                                    c += " "
                                    break
                                else:
                                    input += c

                        if input == 'Transition matrix':

                            while True:

                                c = config.read(1)
                                if c == "[":
                                    index = -1
                                    while True:
                                        c = config.read(1)
                                        if c == "]":

                                            return transition_matrix
                                        if c == "[":
                                            index += 1
                                            while True:
                                                c = config.read(1)
                                                if c == "]":
                                                    matrix = matrix.split(",")
                                                    matrix = self.cast_to_float_vector(matrix)
                                                    transition_matrix[index] = matrix
                                                    matrix = ""
                                                    break
                                                else:
                                                    matrix += c
                        else:
                            input = ""
        except:
            raise IOError


    def cast_to_float_vector(self, vector):
        """
        Method to cast string vector to float vector
        :param vector: input string vector
        :return: float vector
        """
        try:
            for value_index in range(len(vector)):
                value = vector[value_index]
                if isinstance(value, str):

                    value = value.split("/")
                    value = [v.replace("\"", " ").replace("\'", " ") for v in value]
                    if len(value) == 1:
                        value = float(value[0])
                    elif len(value) == 2:
                        value = float(value[0]) / float(value[1])
                    else:
                        raise TypeError

                vector[value_index] = value

            return vector
        except:
            raise TypeError

########################################################################################################################
#                                                                                                                      #
#                                             Parse system input                                                       #
#                                                                                                                      #
########################################################################################################################

    def get_system_configuration(self, configuration_input):
        """
        Function that allows to parse the system input
        :param output_file_path: external file path for swapping mechanism
        :return: adjusted system configuration
        """
        try:
            distributions = [configuration_input[0], configuration_input[1]]
            for distribution in distributions:
                try:
                    for key in distribution.keys():
                        if key in ["rate", "alpha", "beta"]:
                            distribution[key] = float(distribution[key])
                        if key in ["k"]:
                            distribution[key] = int(distribution[key])
                        if key in ["li"]:
                            distribution[key] = np.array(self.cast_to_float_vector(distribution[key].split(",")), dtype=float)
                        if key in ["pi"]:
                            distribution[key] = np.array(self.cast_to_float_vector(distribution[key].split(",")),
                                                         dtype=float)
                        if key in ["maximum"]:
                            if distribution[key] == "None":
                                distribution[key] = None
                            else:
                                distribution[key] = float(distribution[key])
                        if key in ["minimum"]:
                            if distribution[key] == "None":
                                distribution[key] = None
                            else:
                                distribution[key] = float(distribution[key])
                        if key in ["input values", "probabilities"]:
                            if type(distribution[key]) is str:
                                distribution[key] = np.fromstring(distribution[key], sep=',', dtype=float)
                        if key in ["path"]:
                            if distribution[key] is not None:
                                with open(distribution[key], 'r') as conf:
                                    input_data = json.load(conf)
                                    distribution["input values"] = np.array(self.cast_to_float_vector(
                                        input_data["input values"]))
                                    distribution["probabilities"] = np.array(self.cast_to_float_vector(
                                        input_data["probabilities"]))
                                    conf.close()
                except:
                    raise KeyError

            service_time = configuration_input[2]
            Qmax = configuration_input[3]
            transition_functions = self.get_transition_function(configuration_input[4])
            transition_functions = [
                transition_function.replace("service_time", str(service_time)).replace("Qmax", str(Qmax))
                                   for transition_function in transition_functions]
            system_configuration = [*distributions, service_time, Qmax, transition_functions]
            return system_configuration
        except:
            raise IOError





########################################################################################################################
#                                                                                                                      #
#                                             Parse functional input                                                   #
#                                                                                                                      #
########################################################################################################################


    def parse_forward_input(self, configuration=None,
                            input_file_path=None,
                            output_file_path=None,
                            num_project=0,
                            num_mc=0):
        """
        Method to parse the functional Markov chain input
        :param configuration: optional configuration of the Markov chain
        :param input_file_path: optional file path
        :param output_file_path: optional output file path for swapping mechanisms
        :param num_project: number of the current project
        :param num_mc: number of the current Markov chain
        :return: parsed Markov chain
        """
        try:
            if output_file_path is None:
                output_file_path = "./resources/outsourced_calculation/"
            if configuration:
                self._configuration_data = configuration
            else:
                try:
                    self._load_configuration(input_file_path)
                except:
                    self._configuration_file = input_file_path
                    self._configuration_data = {}
                    raise MemoryError
            try:
                states = self._get_states_fa()
            except:
                states = self._get_states_fa(output_file_path)
            state_space_names = self._get_state_space_names()
            try:
                state_designations = self._get_state_designation_fa()
            except:
                state_designations = self._get_state_designation_fa(output_file_path)
            try:
                initial_state_vector = self._get_initial_state_vector_fa()
            except:
                initial_state_vector = self._get_initial_state_vector_fa(output_file_path)
            try:
                factors = self._get_factors()
            except:
                factors = self._get_factors(output_file_path)
            factor_space_names = self._get_factor_space_names()
            try:
                factor_distribution = self._get_factor_probabilities()
            except:
                factor_distribution = self._get_factor_probabilities(output_file_path)
            transition_function = self._get_transition_function(num_project, num_mc)

            return states, state_space_names, state_designations, initial_state_vector, factors, factor_space_names, \
                   factor_distribution, transition_function
        except:
            raise IOError

    def _get_states_fa(self, output_file_path=None):
        """
        Function that allows to read the state space input
        :param output_file_path: external file path for swapping mechanism
        :return: array of states
        """
        try:
            states_list = []
            if output_file_path is None:
                states = self._configuration_data["States"]
                for states in states:
                    if type(states) is list:
                        states_list.append(np.array(states, dtype=float))
                    elif "range" in states:
                        try:
                            states_list.append(np.array(self._str2tuple(states), dtype=float))
                        except:
                            raise IOError
                    elif states != "":
                        if isinstance(states, str):
                            curr_states = [v.replace("-", "(") for v in states.replace("(", "(-").split("(")]
                            if len(curr_states) >= 2:
                                curr_states.remove("")
                                states_list.append([self._str2tuple(re.sub(r'\).*',')', state)) for state in curr_states])
                            else:
                                states_list.append(np.array(self.cast_to_float_vector(curr_states[0].split(",")), dtype=float))
                return states_list
            else:
                state_vector = []
                input = ""
                with open(self._configuration_file) as config:
                    i = 0
                    while True:
                        i += 1
                        c = config.read(1)
                        if c != "":
                            i = 0
                        if i >= 20000:
                            raise IOError
                        if c == "\"" or c == "\'":
                            input = ""
                            while True:
                                c = config.read(1)
                                if c == "\"" or c == "\'":
                                    c += " "
                                    break
                                else:
                                    input += c

                        if input == 'States':
                            while True:
                                c = config.read(1)
                                if c == "[":
                                    bricks = 1
                                    states = ""
                                    while True:
                                        c = config.read(1)

                                        if c == "[":
                                            bricks += 1
                                        elif c == "]":
                                            bricks -= 1
                                            state_vector.append(states.replace("\n", "").replace("\t", ""))
                                            states = ""
                                        else:
                                            states += c
                                        if bricks == 0:

                                            for states in state_vector[:-1]:
                                                if states != "":
                                                    if "range" in states:
                                                        states = states.replace("\"", "")
                                                        states_list.append(np.array(self._str2tuple(states), dtype=float)
                                                            )

                                                    elif isinstance(states, str):
                                                        curr_states = [v.replace("-", "(") for v in
                                                                       states.replace("(", "(-").split("(")]

                                                        if len(curr_states) >= 2:
                                                            curr_states = [state for state in [state.replace(" ", "") for state in curr_states] if state not in ["", ","]]

                                                            states_mem = np.memmap(self.get_memmap_path(output_file_path),
                                                                      dtype=float, mode='w+',
                                                                      shape=len(curr_states))[:] = [self._str2tuple(re.sub(r'\).*', ')', state)) for state in
                                                             curr_states][:]
                                                            del curr_states
                                                            states_list.append(states_mem)
                                                        else:
                                                            states_mem = np.memmap(
                                                                self.get_memmap_path(output_file_path),
                                                                dtype=float, mode='w+',
                                                                shape=len(curr_states))[:] = np.array(
                                                                self.cast_to_float_vector((curr_states[0])[1:-1].split(",")),
                                                                dtype=float)[:]
                                                            states_list.append(states_mem)
                                            return states_list
        except:
            raise IOError

    def _str2tuple(self, state):
        """
        Method that allows to parse a string to tuple
        :param state: represented as string
        :return: state of type tuple
        """
        try:
            return eval(state)
        except:
            raise TypeError

    def _get_state_space_names(self):
        """
        Function that allows to read the state space name input
        :return: list of state space names
        """
        try:
            if self._configuration_data:
                return self._configuration_data["State space names"]
            else:
                ssn = ""
                input = ""
                with open(self._configuration_file) as config:
                    i = 0
                    while True:

                        i += 1

                        c = config.read(1)
                        if c != "":
                            i = 0
                        if i >= 20000:
                            raise IOError
                        if c == "\"" or c == "\'":
                            while True:
                                c = config.read(1)
                                if c == "\"" or c == "\'":
                                    c += " "
                                    break
                                else:
                                    input += c
                        if input == 'State space names':
                            while True:
                                c = config.read(1)
                                if c == "N" or c == "n":
                                    return None
                                if c == "[":
                                    while True:
                                        c = config.read(1)
                                        if c == "]":
                                            ssn = ssn.split(",")
                                            ssn = [str(v).replace("\"", " ").replace("\'", " ") for v in
                                                                 ssn]
                                            return ssn
                                        else:
                                            ssn += c
                        else:
                            input = ''
        except:
            raise IOError

    def _get_state_designation_fa(self, output_file_path=None) -> list or None:
        """
        Function that allows to read the state space designations
        :param output_file_path: external file path for swapping mechanism
        :return: list of state designations
        """
        try:
            if output_file_path is None:
                state_designation = self._configuration_data["State designations"]
                if type(state_designation) is list:
                    if len(state_designation) == 1:
                        return state_designation[0].split(",")
                    else:
                        return state_designation
                elif state_designation is None:
                    return None
                else:
                    raise NotImplementedError
            else:
                state_designation = ""
                input = ""
                with open(self._configuration_file) as config:
                    i = 0
                    while True:

                        i += 1

                        c = config.read(1)
                        if c != "":
                            i = 0
                        if i >= 20000:
                            raise IOError

                        if c == "\"" or c == "\'":
                            while True:
                                c = config.read(1)
                                if c == "\"" or c == "\'":
                                    c += " "
                                    break
                                else:
                                    input += c
                        if input == 'State designations':
                            while True:
                                c = config.read(1)
                                if c == "N" or c == "n":
                                    return None
                                if c == "[":
                                    while True:
                                        c = config.read(1)
                                        if c == "]":
                                            state_designation = state_designation.split(",")
                                            state_designation = [str(v).replace("\"", " ").replace("\'", " ") for v in state_designation]
                                            state_designation = np.memmap(
                                                self.get_memmap_path(output_file_path),
                                                dtype=float, mode='w+',
                                                shape=len(state_designation))[:] = state_designation[:]
                                            return state_designation
                                        else:
                                            state_designation += c
                        else:
                            input = ''
        except:
            raise IOError


    def _get_initial_state_vector_fa(self, output_file_path=None):
        """
        Function that allows to read initial state probabilities
        :param output_file_path: external file path for swapping mechanism
        :return: array of state probabilities
        """
        try:
            if output_file_path is None:
                isv = self._configuration_data["Initial state vector"]
                isv = isv[0]
                if type(isv[0]) is str:
                    isv = self.cast_to_float_vector(isv.split(","))
                return np.array(isv, dtype=float)
            else:
                isv = ""
                input = ""
                with open(self._configuration_file) as config:
                    i = 0
                    while True:

                        i += 1

                        c = config.read(1)
                        if c != "":
                            i = 0
                        if i >= 20000:
                            raise IOError
                        if c == "\"" or c == "\'":
                            while True:
                                c = config.read(1)
                                if c == "\"" or c == "\'":
                                    c += " "
                                    break
                                else:
                                    input += c
                        if input == 'Initial state vector':
                            while True:
                                c = config.read(1)
                                if c == "N" or c == "n":
                                    return None
                                if c == "[":
                                    while True:
                                        c = config.read(1)
                                        if c == "]":
                                            isv = isv.split(",")
                                            isv = [str(v).replace("\"", " ").replace("\'", " ") for v in
                                                                 isv]
                                            isv = np.memmap(
                                                self.get_memmap_path(output_file_path),
                                                dtype=float, mode='w+',
                                                shape=len(isv))[:] = self.cast_to_float_vector(isv)[:]

                                            return np.array(self.cast_to_float_vector(isv), dtype=float)
                                        else:
                                            isv += c

                        else:
                            input = ''
        except:
            raise IOError

    def _get_factor_space_names(self):
        """
        Function that allows to read the factor space name input
        :return: list of factor space names
        """
        try:
            if self._configuration_data:
                return self._configuration_data["Factor space names"]
            else:
                fsn = ""
                input = ""
                with open(self._configuration_file) as config:
                    i = 0
                    while True:

                        i += 1

                        c = config.read(1)
                        if c != "":
                            i = 0
                        if i >= 20000:
                            raise IOError
                        if c == "\"" or c == "\'":
                            while True:
                                c = config.read(1)
                                if c == "\"" or c == "\'":
                                    c += " "
                                    break
                                else:
                                    input += c
                        if input == 'Factor space names':
                            while True:
                                c = config.read(1)
                                if c == "N" or c == "n":
                                    return None
                                if c == "[":
                                    while True:
                                        c = config.read(1)
                                        if c == "]":
                                            fsn = fsn.split(",")
                                            fsn = [str(v).replace("\"", " ").replace("\'", " ") for v in
                                                   fsn]
                                            return fsn
                                        else:
                                            fsn += c
                        else:
                            input = ''
        except:
            raise IOError


    def _get_factors(self, output_file_path=None):
        """
        Function that allows to read the factor input
        :param output_file_path: external file path for swapping mechanism
        :return: array of factors
        """
        try:
            if output_file_path is None:
                factors_list = []
                factors = self._configuration_data["Factors"]
                for factors in factors:
                    if type(factors) is list:
                        if type(factors[0]) is tuple:
                            factors_list.append(factors)
                        else:
                            factors_list.append(np.array(factors, dtype=float))
                    elif factors != "":
                        if isinstance(factors, str):
                            curr_factors = [v.replace("-", "(") for v in factors.replace("(", "(-").split("(")]
                            if len(curr_factors) >= 2:
                             curr_factors.remove("")
                             factors_list.append([self._str2tuple(re.sub(r'\).*', ')', state)) for state in curr_factors])

                            else:
                                factors_list.append(np.array(self.cast_to_float_vector(curr_factors[0].split(",")), dtype=float))


                return factors_list
            else:
                factors_list = []
                input = ""
                with open(self._configuration_file) as config:
                    i = 0
                    while True:

                        i += 1

                        c = config.read(1)
                        if c != "":
                            i = 0
                        if i >= 20000:
                            raise IOError

                        if c == "\"" or c == "\'":
                            input = ""
                            while True:
                                c = config.read(1)
                                if c == "\"" or c == "\'":
                                    c += " "
                                    break
                                else:
                                    input += c

                        if input == 'Factors':
                            while True:
                                c = config.read(1)
                                if c == "[":
                                    bricks = 1
                                    factors = ""
                                    while True:
                                        c = config.read(1)

                                        if c == "[":
                                            bricks += 1
                                            factors = ""
                                        elif c == "]":
                                            bricks -= 1
                                            factors_list.append(factors.replace("\n", "").replace("\t", ""))
                                            factors = ""
                                        else:
                                            factors += c
                                        if bricks == 0:
                                            factor_output = []
                                            for factors in factors_list[:-1]:
                                                if factors != "":
                                                    if isinstance(factors, str):
                                                        curr_factors = [v.replace("-", "(") for v in
                                                                       factors.replace("(", "(-").split("(")]

                                                        if len(curr_factors) >= 2:
                                                            curr_factors = [factor for factor in
                                                                           [factor.replace(" ", "") for factor in curr_factors]
                                                                           if factor not in ["", ","]]
                                                            curr_factors =  np.memmap(
                                                                                self.get_memmap_path(output_file_path),
                                                                                dtype=float, mode='w+',shape=len(curr_factors))[:]\
                                                                = self.cast_to_float_vector([self._str2tuple(re.sub(r'\).*', ')', factor)) for factor in
                                                                 curr_factors])[:]
                                                            factor_output.append(curr_factors
                                                                )
                                                        else:
                                                            curr_factors = np.memmap(
                                                                self.get_memmap_path(output_file_path),
                                                                dtype=float, mode='w+', shape=len(curr_factors))[:] \
                                                                = self.cast_to_float_vector(
                                                                    (curr_factors[0]).split(","))[:]
                                                            factor_output.append(curr_factors)
                                            return factor_output
        except:
            raise IOError

    def _get_factor_probabilities(self, output_file_path=None):
        """
        Method to parse the factor probability input
        :param output_file_path: external file path for swapping mechanism
        :return: array of factor probabilities
        """
        try:
            if output_file_path is None:
                factor_probabilities = self._configuration_data["Factor probabilities"]
                factors_probability_list = []
                for factor_probabilities in factor_probabilities:
                    if factor_probabilities != "":

                        factors_probability_list.append(np.array(self.cast_to_float_vector(factor_probabilities.split(",")), dtype=float))
                return factors_probability_list
            else:
                factors_prob_list = []
                input = ""
                with open(self._configuration_file) as config:
                    i = 0
                    while True:

                        i += 1

                        c = config.read(1)
                        if c != "":
                            i = 0
                        if i >= 20000:
                            raise IOError
                        if c == "\"" or c == "\'":
                            input = ""
                            while True:
                                c = config.read(1)
                                if c == "\"" or c == "\'":
                                    c += " "
                                    break
                                else:
                                    input += c

                        if input == 'Factor probabilities':
                            while True:
                                c = config.read(1)
                                if c == "[":
                                    bricks = 1
                                    factors_prob = ""
                                    while True:

                                        c = config.read(1)

                                        if c == "[":
                                            bricks += 1
                                            factors_prob = ""
                                        elif c == "]":
                                            bricks -= 1
                                            factors_prob_list.append(factors_prob.replace("\n", "").replace("\t", ""))
                                            factors_prob = ""
                                        else:
                                            factors_prob += c
                                        if bricks == 0:
                                            factor_prob_output = []
                                            for factors_prob in factors_prob_list[:-1]:
                                                if factors_prob != "":
                                                    factors_prob = np.memmap(
                                                        self.get_memmap_path(output_file_path),
                                                        dtype=float, mode='w+', shape=len(factors_prob))[:] \
                                                        =  self.cast_to_float_vector(
                                                            (factors_prob).split(","))[:]
                                                    factor_prob_output.append(factors_prob)
                                            return factor_prob_output
        except:
            raise TypeError




    def _get_transition_function(self, num_project, num_mc):
        """
        Method to create the transition functions
        :param num_project: number of the current project
        :param num_mc: number of the current Markov chain
        :return: list of transition functions
        """
        try:
            if self._configuration_data:
                transition_functions = self._configuration_data["Transition functions"]
            else:
                transition_functions = self.parse_transition_function()
            if isinstance(transition_functions[0], str):
                transition_functions = [tf.split('\n') for tf in transition_functions]
            self.create_new_transition_function(transition_functions, num_project, num_mc)
            index = 1
            file_path = 'FunSpec4DTMC.model.parser.transition_functions.project{num_project}.mc{num_mc}.TransitionFunctions'.format(
                num_project=num_project, num_mc=num_mc)
            import sys
            sys.path.append(file_path)
            return file_path
        except:
            raise IOError


    def parse_transition_function(self):
        """
        method to parse the transition functions
        :return: list of transition functions
        """
        try:
            transition_functions_list = []
            input = ""
            with open(self._configuration_file) as config:
                i = 0
                while True:

                    i += 1

                    c = config.read(1)
                    if c != "":
                        i = 0
                    if i >= 20000:
                        raise IOError
                    if c == "\"" or c == "\'":
                        input = ""
                        while True:

                            c = config.read(1)
                            if c == "\"" or c == "\'":
                                c += " "
                                break
                            else:
                                input += c
                    if input == 'Transition functions':
                        while True:
                            c = config.read(1)
                            if c == "[":
                                bricks = 1
                                transition_functions = ""
                                while True:
                                    c = config.read(1)
                                    if c == "[":
                                        bricks +=1
                                    elif c == "]":
                                        bricks -= 1
                                    elif bricks == 0:
                                        return transition_functions_list

                                    if c == "\"":
                                        transition_functions = ""
                                        c = config.read(1)
                                        while c != "\"":
                                            transition_functions += c
                                            c = config.read(1)

                                        transition_functions_list.append(transition_functions)

                        else:
                            input = ''
        except:
            raise IOError

    def create_new_transition_function(self, function, number_project, number_mc):
        """
        Method to create a new transition funtion from string
        :param function: function represented as string
        :param number_project: number of the current project
        :param number_mc: number of the current Markov chain
        :return:
        """
        try:
            file_paths = ['./FunSpec4DTMC/model/parser/transition_functions/project{num_project}/mc{num_mc}/TransitionFunctions.py'.format(
                    num_project=number_project, num_mc=number_mc),
                './FunSpec4DTMC/model/parser/transition_functions/project{num_project}/mc{num_mc}/TransitionFunctions.pyx'.format(
                    num_project=number_project, num_mc=number_mc)]
            for file_path in file_paths:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as transition_function:
                    transition_function.write('\n')
                    for tf in function:
                        for line in tf:
                            transition_function.write(line + '\n')
                    transition_function.close()
        except:
            raise IOError

        try:
            import cython

            file_path = "FunSpec4DTMC/model/parser/transition_functions/project{num_project}/mc{num_mc}/" \
                .format(num_project=number_project, num_mc=number_mc)


            compiling_transition_function = subprocess.Popen(
                'python ./FunSpec4DTMC/model/parser/setup.py build_ext  --build-lib={fp}  --curr={num_project},{num_mc} clean'.format(
                    fp=file_path, num_project=number_project, num_mc=number_mc))

            compiling_transition_function.wait()
        except:
            raise FileExistsError

    def get_transition_function(self, transition_functions: str):
        """
        Method to get the separated transition functions from string
        :param transition_functions: transition functions represented as string
        :return: transition functions represented as list of the separated transition functions
        """

        transition_functions = transition_functions.replace("cpdef", "XXX _XX_ ")
        transition_functions = re.split("(def)|(XXX)", transition_functions)
        transition_functions = [tf for tf in transition_functions if tf is not None and ("transition_function" in tf)]
        results = []
        for tf in transition_functions:
            if "_XX_" in tf:
                results.append(tf.replace("_XX_", "cpdef"))
            else:
                results.append("def " + tf)
        return results




########################################################################################################################
#                                                                                                                      #
#                                             Save MC                                                                  #
#                                                                                                                      #
########################################################################################################################

    @staticmethod
    def save_functional_mc_input(markov_chain_input, file_path):
        """
        Method to store functional Markov chain input to memory
        :param markov_chain_input: Markov chain input to store
        :param file_path: external file used as storage path
        """
        try:
            if len(markov_chain_input[0]) == 1:
                config = {"States": [list(states) for states in markov_chain_input[0]],
                          "State space names": ["StateDim0", "StateDim1", "StateDim2"],
                          "State designations":   markov_chain_input[1],
                          "Initial state vector":  list(markov_chain_input[2]),
                          "Factor space names": ["FactorDim0", "FactorDim1", "FactorDim2"],
                          "Factors": [list(factors) for factors in (markov_chain_input[3])],
                          "Factor probabilities": [list(factor_probabilities) for factor_probabilities
                                                   in (markov_chain_input[4])]
                          }
            else:
                config = {"States": [list(states) for states in markov_chain_input[0]],
                          "State space names": ["StateDim0", "StateDim1", "StateDim2"],
                          "State designations": markov_chain_input[1],
                          "Initial state vector": list(markov_chain_input[2]),
                          "Factor space names": ["FactorDim0", "FactorDim1", "FactorDim2"],
                          "Factors": [list(factors) for factors in (markov_chain_input[3])[0]],
                          "Factor probabilities": [list(factor_probabilities) for factor_probabilities
                                                   in (markov_chain_input[4])[0]]
                          }
            transition_functions = markov_chain_input[5]
            tf_output = []
            for transition_function in transition_functions:
                lines = transition_function.strip().split("\n")

                lines = [line for line in lines if line != ""]
                tf_output.append(lines)
            config["Transition functions"] = tf_output
            with open(file_path, 'w') as fp:
                json.dump(config, indent=2, separators=(',', ': '), fp=fp)
        except:
            raise IOError


    def save_functional_mc(self, markov_chain, file_path):
        """
        Method to store functional Markov chain to memory
        :param markov_chain: Markov chain to store
        :param file_path: external file used as storage path
        """
        try:
            if len(markov_chain.get_states()) == 1:
                config = {"States": [list(states) for states in markov_chain.get_states()],
                          "State space names": list(markov_chain.get_state_space_names()),
                          "State designations": markov_chain.get_state_designations(),
                          "Initial state vector": list(markov_chain.get_initial_state_vector()),
                          "Factors": [[list(factors) for factors in markov_chain.get_factors()[0]]],
                          "Factor space names": list(markov_chain.get_factor_space_names()),
                          "Factor probabilities": [list(factor_probabilities) for factor_probabilities
                                                   in markov_chain.get_factor_distributions()]
                          }
            else:
                config = {"States": [list(states) for states in markov_chain.get_states()],
                          "State space names": list(markov_chain.get_state_space_names()),
                          "State designations": markov_chain.get_state_designations(),
                          "Initial state vector": list(markov_chain.get_initial_state_vector()),
                          "Factors": [list(factors) for factors in markov_chain.get_factors()],
                          "Factor space names": list(markov_chain.get_factor_space_names()),
                          "Factor probabilities": [list(factor_probabilities) for factor_probabilities
                                                   in markov_chain.get_factor_distributions()]
                          }
            transition_functions = markov_chain.get_transition_functions()
            fun = transition_functions.replace(".", "/") + ".py"
            with open(fun, "r+") as f:
                    tf = f.read()
            f.close()
            transition_functions = self.get_transition_function(tf)
            config["Transition functions"] = transition_functions
            with open(file_path, 'w') as fp:
                json.dump(config, indent=2, separators=(',', ': '), fp=fp)
        except:

            raise IOError

    @staticmethod
    def save_conventional_mc(markov_chain, file_path):
        """
        Method to store conventional Markov chain input to memory
        :param markov_chain: Markov chain to store
        :param file_path: external file used as storage path
        """
        print("hier")
        print(list(markov_chain.get_initial_state_vector()))
        print(list(markov_chain.get_transition_matrix()))
        print(list(markov_chain.get_state_designations()))

        try:
            config = {'Initial state vector': list(markov_chain.get_initial_state_vector()),
                      'Transition matrix': [line.tolist() for line in list(markov_chain.get_transition_matrix())]
                      }
            if markov_chain.get_state_designations() is None:
                config["State designations"] = None
            else:
                config["State designations"] = list(markov_chain.get_state_designations())
            with open(file_path, 'w') as fp:
                json.dump(config,
                          indent=4, separators=(',', ': '), fp=fp)
        except:
            raise IOError

    @staticmethod
    def save_matrix(matrix, file_path):
        """
        Method to store matrix to memory
        :param matrix: matrix to store
        :param file_path: external file used as storage path
        """
        try:
            config = {'Transition matrix': matrix.tolist()}
            with open(file_path, 'w') as fp:
                json.dump(config,
                          indent=4, separators=(',', ': '), fp=fp)
        except:
            raise IOError

    @staticmethod
    def save_vector(vector, file_path):
        """
        Method to store vector to memory
        :param vector: vector to store
        :param file_path: external file used as storage path
        """
        try:
            config = {'Stationary state vector': vector.tolist()}
            with open(file_path, 'w') as fp:
                json.dump(config,
                          indent=4, separators=(',', ': '), fp=fp)
        except:
            raise IOError


########################################################################################################################
#                                                                                                                      #
#                                             Memmap Files                                                             #
#                                                                                                                      #
########################################################################################################################


    def get_memmap_path(self, output_file_path: str):
        """
        Mthod used for getting the file path for memory file path files
        :param output_file_path: external file used for swapping
        """

        index = 0
        while os.path.isfile(output_file_path + "memmap" + str(index) + ".fs"):

            index += 1
        return output_file_path + "memmap" + str(index) + ".fs"




########################################################################################################################
#                                                                                                                      #
#                                             Methods for rendering matrices, vectors and factors                      #
#                                                                                                                      #
########################################################################################################################


    def get_mc_visualisations(self, markov_chains, results, number_project=None, number_mc=None):
        """
        Method to get a visualization of a Markov chain
        :param markov_chains: markov chain input
        :return: visualization of the Markov chain
        """
        for mc in markov_chains:
            if mc.get_type() == 'MarkovChainConventionalApproach':
                results.append(self.get_conventional_mc_visualisation(mc))

            elif mc.get_type() == 'MarkovChainForwardApproach':
                results.append(self.get_functional_mc_visualisation(mc, number_project, number_mc))
        return results


    def get_conventional_mc_visualisation(self, markov_chain):
        """
        Method to get a visualization of a conventional specified Markov chain
        :param markov_chains: markov chain input
        :return: visualization of the Markov chain
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [1, 2]})
        ax1.set_title("Initial state vector", fontsize=16, loc='left')
        ax1.spines["left"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["bottom"].set_visible(False)
        ax1.spines["top"].set_visible(False)
        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)

        isv = markov_chain.get_initial_state_vector()
        if len(isv) > 10:
            vector = np.concatenate((isv[0:5], [4.0]))
            vector = np.concatenate((vector, isv[-5:]))

        else:
            vector = isv

        layout, input = self.get_latexarray(vector)
        ax1.text(0.5, 0.5,
                 r'$\left( \begin{array}' + layout + r' {input} \end{{array}}\right)$'.format(input=input),
                 verticalalignment='center',
                 horizontalalignment='center',
                 fontsize=16)

        ax2.set_title("Transition matrix", loc='left', fontsize=16)
        ax2.spines["left"].set_visible(False)
        ax2.spines["right"].set_visible(False)
        ax2.spines["bottom"].set_visible(False)
        ax2.spines["top"].set_visible(False)
        ax2.get_xaxis().set_visible(False)
        ax2.get_yaxis().set_visible(False)

        tm = markov_chain.get_transition_matrix()


        if len(tm[0]) > 10:
            matrix = []
            for i in range(5):
                line = []
                for j in range(5):
                    line.append(tm[i, j])
                line.append(4.0)
                for j in range(-5, 0):
                    line.append(tm[i, j])
                matrix.append(line)

            matrix.append([3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0])

            for i in range(-5, 0):
                line = []
                for j in range(5):
                    line.append(float(tm[i, j]))
                line.append(4.0)
                for j in range(-5, 0):
                    line.append(float(tm[i, j]))
                matrix.append(line)
        else:
            matrix = tm

        layout, input = self.get_latexarray(np.array(matrix), 2)
        ax2.text(0.5, 0.5,
                 r'$\left( \begin{array}' + layout + r' {input} \end{{array}}\right)$'.format(input=input),
                 verticalalignment='center',
                 horizontalalignment='center',
                 fontsize=16
                 )
        return fig

    def get_functional_mc_visualisation(self, markov_chain, number_project, number_mc):
        """
        Method to get a visualization of a functional specified Markov chain
        :param markov_chains: markov chain input
        :return: visualization of the Markov chain
        """

        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111)

        initial_states = markov_chain.get_states()[0]
        state_space_names = markov_chain.get_state_space_names()
        if type(initial_states[0]) is tuple or type(initial_states[0]) is list or type(initial_states[0]) is np.ndarray:
            if len(initial_states) > 40:
                ax1.text(0.5, 0.5, "Too many state tuples have been entered for an appropriate representation.",
                         verticalalignment='center',
                         horizontalalignment='center',
                         fontsize=16
                         )
            else:
                x_values = initial_states
                y_values = markov_chain.get_initial_state_vector()
                ax1.plot(range(1, len(x_values)+1), y_values, '.', label=state_space_names[0])
                ax1.set_xticks(range(1, len(x_values)+1))
                ax1.set_xticklabels(x_values, rotation=90)
                ax1.set_ylabel('State probabilities')
                ax1.set_xlabel('States')

        else:
            x_values = initial_states
            y_values = markov_chain.get_initial_state_vector()
            ax1.plot(x_values, y_values, '.', label=state_space_names[0])
            ax1.set_xticks(x_values)
            ax1.set_ylabel('State probabilities')
            ax1.set_xlabel('States')
        ax1.legend()
        fig2 = plt.figure()

        ax2 = fig2.add_subplot(111)

        factors = markov_chain.get_factors()
        factor_space_names = markov_chain.get_factor_space_names()

        factor_probabilities = markov_chain.get_factor_distributions()
        factor_map = {}
        i = 0

        for index in range(len(factors)):
            if type((factors[index])[0]) is tuple or type((factors[index])[0]) is list or type((factors[index])[0]) is np.ndarray:
                for factor in factors[index]:
                    if not str(factor) in factor_map:
                        factor_map[str(factor)] = i
                        i += 1

                if len(factors[index]) > 40:
                    ax2.text(0.5, 0.5, "Too many factor tuples have been entered for an appropriate representation.",
                             verticalalignment='center',
                             horizontalalignment='center',
                             fontsize=16
                             )
                    ax2.spines["left"].set_visible(False)
                    ax2.spines["right"].set_visible(False)
                    ax2.spines["bottom"].set_visible(False)
                    ax2.spines["top"].set_visible(False)
                    ax2.get_xaxis().set_visible(False)
                    ax2.get_yaxis().set_visible(False)
                    break
                else:
                    indices = [factor_map[str(factor)] for factor in factors[index]]
                    ax2.plot(indices, factor_probabilities[index], '.', label=factor_space_names[index])
                    ax2.set_xticks(list(factor_map.values()))
                    ax2.set_xticklabels(list(factor_map.keys()), rotation=90)
                    ax2.set_xlabel('Factors')
                    ax2.set_ylabel('Factor probabilities')
            else:
                ax2.plot(factors[index], factor_probabilities[index], '.', label=factor_space_names[index])
                ax2.set_xlabel('Factors')
                ax2.set_ylabel('Factor probabilities')
        ax2.legend()
        filepath = './FunSpec4DTMC/model/parser/transition_functions/project{num_project}/mc{num_mc}/TransitionFunctions.py'.format(
                num_project=number_project, num_mc=number_mc)
        with open(filepath, "r+") as f:
            transition_function = f.read()
        f.close()
        transition_functions = self.get_transition_function(transition_function)
        result = (fig1, fig2, transition_functions)
        return result

    def vector_plot(self, vector):
        """
        Method to get a vector plot from array input
        :param vector: input vector
        :return: vector plot
        """
        fig, ax1 = plt.subplots(1, 1)
        ax1.set_title("Stationary state vector", loc='left', fontsize=16)
        ax1.spines["left"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["bottom"].set_visible(False)
        ax1.spines["top"].set_visible(False)
        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)


        if len(vector) > 10:
            truncated_vector = np.concatenate((vector[0:5], [4.0]))
            truncated_vector = np.concatenate((truncated_vector, vector[-5:]))

        else:
            truncated_vector = vector

        layout, input = self.get_latexarray(truncated_vector)
        ax1.text(0.5, 0.5,
                    r'$\left( \begin{array}' + layout + r' {input} \end{{array}}\right)$'.format(input=input),
                    verticalalignment='center',
                    horizontalalignment='center',
                    fontsize=16)

        return fig

    def matrix_plot(self, matrix):
        """
        Method to get a matrix plot from array input
        :param matrix: input matrix
        :return: input matrix
        """
        fig, ax1 = plt.subplots(1, 1)
        ax1.set_title("Transition matrix", loc='left', fontsize=16)
        ax1.spines["left"].set_visible(False)
        ax1.spines["right"].set_visible(False)
        ax1.spines["bottom"].set_visible(False)
        ax1.spines["top"].set_visible(False)
        ax1.get_xaxis().set_visible(False)
        ax1.get_yaxis().set_visible(False)
        tm = matrix

        if len(matrix[0]) > 10:
            matrix = []
            for i in range(5):
                line = []
                for j in range(5):
                    line.append(tm[i, j])
                line.append(4.0)
                for j in range(-5, 0):
                    line.append(tm[i, j])
                matrix.append(line)

            matrix.append([3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0, 3.0])

            for i in range(-5, 0):
                line = []
                for j in range(5):
                    line.append(float(tm[i, j]))
                line.append(4.0)
                for j in range(-5, 0):
                    line.append(float(tm[i, j]))
                matrix.append(line)
        else:
            matrix = tm

        layout, input = self.get_latexarray(np.array(matrix), 2)
        ax1.text(0.5, 0.5,
                 r'$\left( \begin{array}' + layout + r' {input} \end{{array}}\right)$'.format(input=input),
                 verticalalignment='center',
                 horizontalalignment='center',
                 fontsize=16
                 )
        return fig

    def get_latexarray(self, vector, dim=1):
        """
        Method to parse matrix into Latex code
        :param vector: input vector
        :param dim: dimension of the vector
        :return: Latex dode representation of the vector
        """
        if dim == 1:
            vector_length = len(vector)
        elif dim == 2:
            vector_length = len(vector[0])
        else:
            raise TypeError

        layout = r'{'
        for i in range(vector_length):
            layout += r'r'
        layout += r'}'

        vector = np.around(vector, self.display_precision)
        if len(vector.shape) > 2:
            raise ValueError('bmatrix can at most display two dimensions')
        lines = str(vector).replace('[', '').replace(']', '').splitlines()
        data = []
        data += [' , & '.join(l.split()) for l in lines]
        if dim == 1:
            data = r' , & '.join(data)
        else:
            data = r' \\ '.join(data)

        data = data.replace("4.", "...")
        data = data.replace("3.", "...")
        return layout, data

    def plot_period(self, period):
        """
        method to visualize the period of a Markov chain
        :param period:
        :return:
        """
        figure = plt.figure()
        figure.text(0.5, .9,
                    'The period of the Markov chain amounts to {period}.'.format(period=period),
                    verticalalignment='top',
                    horizontalalignment='center',
                    fontsize=16)

        return figure

