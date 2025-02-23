from qiskit import transpile, QuantumCircuit
from bqskit.ir import Circuit
from bqskit.passes import UnfoldPass, ForEachBlockPass, QSearchSynthesisPass, ScanPartitioner
from bqskit.compiler import Compiler
from qiskit.qasm2 import dump
from bqskit.ext import qiskit_to_bqskit, bqskit_to_qiskit, model_from_backend
from qiskit.converters import circuit_to_dag, dag_to_circuit
from predetermined.compile import predeterminedCompilation
from pathlib import Path
import os
from qiskit.qasm2 import dump
from qiskit import transpile

if __name__ =='__main__':
    print('a')


    