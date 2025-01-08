import random 
from circuits.qiskit_circuits import (
    dtc_unitary,
    multi_control_circuit,
    random_clifford_circuit,
    bv_all_ones
)
from qiskit.qasm2 import dump
import time
#construct the diferent benchpress circuits (num qubits, num circuits)

#Folder location that contains the circuits from different frameworks
bench_path = 'benchmark_circuit_folders'


def construct_dtc_unitary(num_qubits: int, num_circuits: int):
  """Generates a random Floquet unitary circuit with a random seed and random rotation from [1,9.9999].
  Creates a .qasm file for the circuit, containing the seed, x-rotation, and number of qubits. 
  Parameters:
    num_qubits (int): Required. Number of qubits for the circuit.
    num_circuits (int): Required. Number of circuits to generate. 
  """
  for i in range(num_circuits):
    rand_seed = random.randint(10000, 99999)
    rand_float = rand_seed / 10000
    qc = dtc_unitary(num_qubits=num_qubits, g=rand_float, seed=rand_seed)
    dump(qc, bench_path + '/qiskit/dtc/dtc_' + str(num_qubits) + "_" + str(rand_float) + '_' + str(rand_seed) + '.qasm')

def construct_multi_control_circuit(num_qubits: int):
  """Generates a random circuit with X gates.
  Creates a .qasm file for the circuit, containing the number of qubits. 
  Parameters:
    num_qubits (int): Required. Number of qubits for the circuit.
  """
  qc = multi_control_circuit(num_qubits=num_qubits)
  dump(qc, bench_path + '/qiskit/multi_control/multi_control_' + str(num_qubits) + '.qasm')
    
def construct_clifford_circuit(num_qubits: int, num_circuits: int):
  """Generates a random clifford circuit using a random seed.
  Creates a .qasm file for the circuit, containing the seed and number of qubits. 
  Parameters:
    num_qubits (int): Required. Number of qubits for the circuit.
    num_circuits (int): Required. Number of circuits to generate. 
  """
  for i in range(num_circuits):
    rand_seed = random.randint(10000, 99999)
    qc = random_clifford_circuit(num_qubits=num_qubits, seed=rand_seed)
    dump(qc, bench_path + '/qiskit/clifford/clifford_' + str(num_qubits) + '_' + str(rand_seed) + '.qasm')
 # circuit = QuantumCircuit.from_qasm_file()

      
if __name__ == "__main__":
  nums = [10, 20, 30, 40, 50, 75, 100]
  start_time = time.time()
  
  for num in nums:
    #construct_dtc_unitary(num_qubits=num, num_circuits=10)
    #construct_clifford_circuit(num_qubits=num, num_circuits=10)
    construct_multi_control_circuit(num_qubits=num)
  print(f'Done. Time taken to gener')