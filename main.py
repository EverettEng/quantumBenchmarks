from predetermined.compile import predeterminedCompilation
from bqskit.ir import Circuit
from construct_benchmarks.construct_bqskit_benchmarks import construct_bqskit_random_clifford
from qiskit import QuantumCircuit   
from construct_benchmarks.construct_bqskit_benchmarks import construct_bqskit_multi_control_circuit
import pandas as pd
from pandas import json_normalize
import json
from construct_benchmarks.construct_bqskit_benchmarks import (construct_bqskit_circSU2, 
                                                              construct_bqskit_dtc_unitary, 
                                                              construct_bqskit_QV, 
                                                              construct_bqskit_random_clifford)
from construct_benchmarks.construct_qiskit_benchmarks import (construct_qiskit_clifford_circuit,
                                                              construct_qiskit_dtc_unitary,
                                                              construct_qiskit_multi_control_circuit)


if __name__ == '__main__':
   predeterminedCompilation(qc='benchmark_circuits/sat_n11_transpiled.qasm',
                            json_path='compiled_circuits',
                            save_path='compiled_circuits',
                            replace_filter='always')   
   print('Done')


    
    

    
