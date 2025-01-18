from bqskit_compile.bqskitTests import optimizationAnalysis
from bqskit.ir import Circuit 
import random
import math
from qiskit import QuantumCircuit, transpile
from construct_benchmarks.construct_qiskit_benchmarks import construct_clifford_circuit
from qiskit.transpiler.passes import Depth, Collect2qBlocks
from qiskit.transpiler import PassManager
from qiskit.dagcircuit import DAGCircuit
from qiskit.converters import circuit_to_dag
from qiskit.transpiler.preset_passmanagers import level_1_pass_manager
from bqskit_compile.compile import optimizeBQSkit
from predetermined.compile import predeterminedCompilation

if __name__ == '__main__':
    """
    Test code below 
    
    qc = 'benchmark_circuit_folders/bqskit/su2'
    circuit_save_path = 'benchmark_circuit_folders/optimized_bqskit/su2'
    json_path = 'benchmark_circuit_folders/optimized_bqskit/su2_json'
    optimizeBQSkit(qc=qc,
                    circuit_save_path=circuit_save_path,
                    json_path=json_path,
                    success_threshold=1e-8,
                    partitioner=1,
                    pass_type=1
                   )
    """
    #construct_clifford_circuit(num_qubits=20, num_circuits=2, save_path='benchmark_circuits')

    predeterminedCompilation(qc='benchmark_circuits/clifford_10_98001.qasm',
                            save_path='compiled_circuits',
                            json_path='compiled_circuits',
                            replace_filter='aa'
                            )
    

    
