import sys
from PyQt5 import QtWidgets
import os
import subprocess


def main():
    compile_forward_algorithm()
    from FunSpec4DTMC.FunSpecControler import Simulator
    clear_calculation_data()
    app = QtWidgets.QApplication(sys.argv)
    fs_controler = Simulator()
    clear_calculation_data()
    sys.exit(app.exec_())


def compile_forward_algorithm():
    try:
        print("Cython: Compile Forward Algorithms if Cython exist if it has not yet been done... ")
        file_path = "."
        compiling_transition_function = subprocess.Popen(
            'python ./FunSpec4DTMC/setup.py build_ext  --build-lib={fp} clean'.format(
                fp=file_path))
        compiling_transition_function.wait()
        print("...Installation succeeded!")
    except:
        print("...Cython extension not found!")

def clear_calculation_data():
    path = "./resources/outsourced_calculation/"
    filelist = [f for f in os.listdir(path) if f.endswith(".fs")]
    for f in filelist:
        os.remove(os.path.join(path, f))

if __name__ == "__main__":
    main()