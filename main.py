from predetermined.compile import predeterminedCompilation
from bqskit.ir import Circuit
from qiskit import QuantumCircuit   
from construct_benchmarks.construct_bqskit_benchmarks import construct_bqskit_multi_control_circuit
import pandas as pd
from pandas import json_normalize
import json
from construct_benchmarks.construct_bqskit_benchmarks import (construct_bqskit_circSU2, 
                                                              construct_bqskit_dtc_unitary, 
                                                              construct_bqskit_QV, 
                                                              construct_bqskit_clifford,
                                                              construct_bqskit_bv_all_ones)
from construct_benchmarks.construct_qiskit_benchmarks import (construct_qiskit_clifford_circuit,
                                                              construct_qiskit_dtc_unitary,
                                                              construct_qiskit_multi_control_circuit,
                                                              construct_qiskit_bv_all_ones,
                                                              construct_qiskit_clifford_optimized)
import pandas as pd
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit.transpiler.passes import CountOps
from bqskit.ext import qiskit_to_bqskit
from qiskit import transpile
from qiskit.qasm2 import dump
import os
import time
from qiskit.providers.fake_provider import GenericBackendV2
from qiskit_ibm_runtime.fake_provider import FakeWashingtonV2
from qiskit.transpiler import CouplingMap
import matplotlib.pyplot as plt
from bqskit_compile.compile import optimizeBQSkit
from pathlib import Path

 
if __name__ == '__main__':
    predeterminedCompilation(qc='qasm/benchmark_circuits/feynman',
                            json_path='qasm/optimization_data/feynman',
                            save_path='qasm/compiled_circuits/feynman',
                            replace_filter='less-than-multi',
                            partitioner=1)
    df = pd.read_json('qasm/optimization_data/feynman/feynman_optimized.json')
    df.to_csv('qasm/optimization_data/feynman/Feynman.csv', index=False)
    print('done')
   

    
    

    
