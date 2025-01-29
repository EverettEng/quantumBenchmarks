from predetermined.compile import predeterminedCompilation
from bqskit.ir import Circuit
from construct_benchmarks.construct_bqskit_benchmarks import construct_bqskit_random_clifford
from qiskit import QuantumCircuit
from construct_benchmarks.construct_bqskit_benchmarks import construct_bqskit_multi_control_circuit
import pandas as pd
from pandas import json_normalize
import json

if __name__ == '__main__':
   """
   predeterminedCompilation(qc='benchmark_circuits',
                            save_path='compiled_circuits',
                            json_path='compiled_circuits',
                            partitioner=1,
                            replace_filter='less-than')
   """
   df = pd.read_json('compiled_circuits/benchmark_circuits_optimized.json')
   df.to_csv('compiled_circuits/circuitData.csv', index=False)
      
   


    
    

    
