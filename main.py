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

if __name__ == '__main__':
   #save_path = 'benchmark_circuits/bqskit_QV'
   #for i in range(5,51):
      #construct_bqskit_circSU2(num_qubits=i,num_reps=3,save_path=save_path)
      #construct_bqskit_dtc_unitary(num_qubits=i,num_circuits=5,save_path=save_path)
      #construct_bqskit_QV(num_qubits=i,num_circuits=5,save_path='benchmark_circuits/bqskit_QV')
      #construct_bqskit_clifford(num_qubits=i,num_circuits=5,save_path='benchmark_circuits/bqskit_clifford')
      #construct_bqskit_bv_all_ones(num_qubits=i,save_path='benchmark_circuits/bqskit_bv')
      #construct_qiskit_clifford_circuit(num_qubits=i,num_circuits=5,save_path='benchmark_circuits/qiskit_clifford')
      #construct_qiskit_dtc_unitary(num_qubits=i,num_circuits=5,save_path='benchmark_circuits/qiskit_dtc')
      #construct_qiskit_multi_control_circuit(num_qubits=i,save_path='benchmark_circuits/qiskit_multi_control')
      #construct_qiskit_bv_all_ones(num_qubits=i,num_circuits=5,save_path='benchmark_circuits/qiskit_bv')
      #construct_qiskit_clifford_optimized(num_qubits=i,num_circuits=5,save_path='benchmark_circuits/qiskit_clifford_optimized')
      #continue
   
   
   #predeterminedCompilation(qc='qasm/benchmark_circuits/bqskit_dtc',
   #                         json_path='qasm/optimization_data/bqskit_dtc',
   #                         save_path='qasm/compiled_circuits/bqskit_dtc',
   #                         replace_filter='less-than-multi',
   #                         partitioner=0)
   
   df = pd.read_json('qasm/optimization_data/bqskit_dtc/bqskit_dtc_optimized.json')
   df.to_csv('qasm/optimization_data/bqskit_dtc/BQSkit_DTC_Unitary.csv')
   

    
    

    
