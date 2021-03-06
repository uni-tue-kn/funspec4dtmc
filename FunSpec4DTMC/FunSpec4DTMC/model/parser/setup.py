
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

from Cython.Build import cythonize
from distutils.core import setup
import numpy
import sys


for arg in sys.argv:
    if "--curr=" in arg:
         num_project, num_mc = tuple(map(int, arg.split("=")[1].split(",")))
         sys.argv.remove(arg)

setup(
      include_dirs=[numpy.get_include()],
      ext_modules=cythonize("./FunSpec4DTMC/model/parser/transition_functions/project{num_project}/mc{num_mc}/TransitionFunctions.pyx".format(num_project= num_project, num_mc=num_mc)),
      requires=['Cython', 'matplotlib', 'numpy']
     )
