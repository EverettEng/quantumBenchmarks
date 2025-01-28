import random 
from circuits.qiskit_circuits import (
    dtc_unitary,
    multi_control_circuit,
    random_clifford_circuit
)
from qiskit.qasm2 import dump
import os

def construct_qiskit_dtc_unitary(num_qubits: int, num_circuits: int = 1, save_path: str = None):
  """Generates a random Floquet unitary circuit with a random seed and random rotation from [1,9.9999].
  If a save path is inputted, creates a .qasm file for the circuit, containing the seed, x-rotation, and number of qubits.
  
  Parameters:
    num_qubits (int): Required. Number of qubits for the circuit.
    num_circuits (int): Number of circuits to generate. (Default: 1).
    save_path (str): Path to save the random circuit to. (Default: None)
    
  Returns:
    If num_circuits is more than 1, returns a list of random DTC QuantumCircuits num_circuits long. 
    Otherwise, returns a list containing a random DTC QuantumCircuit and its name.
  """
  
  qc_list = []
  for i in range(num_circuits):
    rand_seed = random.randint(10000, 99999)
    rand_float = rand_seed / 10000
    qc = dtc_unitary(num_qubits=num_qubits, g=rand_float, seed=rand_seed)
    if isinstance(save_path,str) and os.path.isdir(save_path):
      dump(qc, save_path + '/dtc_' + str(num_qubits) + "_" + str(rand_float) + '_' + str(rand_seed) + '.qasm')
    qc_list.append([qc, 'dtc_' + str(num_qubits) + "_" + str(rand_float) + '_' + str(rand_seed) + '.qasm'])
  if num_circuits > 1:
    return qc_list
  else:
    return qc_list[0]
    

def construct_qiskit_multi_control_circuit(num_qubits: int, save_path: str = None):
  """Generates a random circuit with X gates.
  If a save path is inputted, creates a .qasm file for the circuit, containing the number of qubits. 
  
  Parameters:
    num_qubits (int): Required. Number of qubits for the circuit.
    save_path (str): Path to save the random circuit to. (Default: None)
    
  Returns:
    A list containing a multi-control QuantumCircuit and its name.
  """
  qc = multi_control_circuit(num_qubits=num_qubits)
  if isinstance(save_path,str) and os.path.isdir(save_path):
    dump(qc, save_path + '/multi_control_' + str(num_qubits) + '.qasm')
  return [qc, 'multi_control_' + str(num_qubits) + '.qasm']
    
def construct_qiskit_clifford_circuit(num_qubits: int, num_circuits: int = 1, save_path: str = None):
  """Generates a random clifford circuit using a random seed.
  If a save path is inputted, creates a .qasm file for the circuit, containing the seed and number of qubits.
   
  Parameters:
    num_qubits (int): Required. Number of qubits for the circuit.
    num_circuits (int): Number of circuits to generate. (Default: 1)
    save_path (str): Path to save the random circuit to. (Default: None)
    
  Returns:
    If num_circuits is more than 1, returns a list of random Clifford QuantumCircuits num_circuits long. 
    Otherwise, returns a list containing a random Clifford QuantumCircuit and its name.
  """
  qc_list = []
  for i in range(num_circuits):
    rand_seed = random.randint(10000, 99999)
    qc = random_clifford_circuit(num_qubits=num_qubits, seed=rand_seed)
    if isinstance(save_path,str) and os.path.isdir(save_path):
      dump(qc, save_path + '/clifford_' + str(num_qubits) + '_' + str(rand_seed) + '.qasm')
    qc_list.append([qc,'clifford_' + str(num_qubits) + '_' + str(rand_seed) + '.qasm' ])
  if num_circuits > 1:
    return qc_list
  else:
    return qc_list[0]
