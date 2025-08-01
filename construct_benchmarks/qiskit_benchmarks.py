import random 
from circuits.qiskit_circuits import (
    dtc_unitary,
    multi_control_circuit,
    random_clifford_circuit,
    bv_all_ones,
    random_clifford_optimized
)
from qiskit.qasm2 import dump
import os
import platform

def construct_qiskit_dtc_unitary(num_qubits: int, num_circuits: int = 1, save_path: str = None, seed: int = None):
  """Generates a random Floquet unitary circuit with a random seed and random rotation from [1,9.9999].
  If a save path is inputted, creates a .qasm file for the circuit, containing the seed, x-rotation, and number of qubits.
  
  Parameters:
    num_qubits (int): Required. Number of qubits for the circuit.
    num_circuits (int): Number of circuits to generate. (Default: 1).
    save_path (str): Path to save the random circuit to. (Default: None)
    seed (int): Manual seed for the quantum circuit. If no seed is inputted, one will be generated. (Default: None)
    
  Returns:
    If num_circuits is more than 1, returns a list of lists of random DTC QuantumCircuits and their names num_circuits long. 
    Otherwise, returns a list containing a random DTC QuantumCircuit and its name.
  """
  if platform.system() == 'Windows' and save_path is not None:
    save_path = save_path.replace('\\', '/')
  qc_list = []
  for i in range(num_circuits):
    if seed == None:
      rand_seed = random.randint(10000, 99999)
    else:
      rand_seed = seed
    rand_float = rand_seed / 10000
    qc = dtc_unitary(num_qubits=num_qubits, g=rand_float, seed=rand_seed)
    if isinstance(save_path,str) and os.path.isdir(save_path):
      dump(qc, save_path + '/qiskit_dtc_' + str(num_qubits) + "_" + str(rand_float) + '_' + str(rand_seed) + '.qasm')
    qc_list.append([qc, 'qiskit_dtc_' + str(num_qubits) + "_" + str(rand_float) + '_' + str(rand_seed) + '.qasm'])
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
  if platform.system() == 'Windows' and save_path is not None:
    save_path = save_path.replace('\\', '/')
  qc = multi_control_circuit(num_qubits=num_qubits)
  if isinstance(save_path,str) and os.path.isdir(save_path):
    dump(qc, save_path + '/qiskit_multi_control_' + str(num_qubits) + '.qasm')
  return [qc, 'qiskit_multi_control_' + str(num_qubits) + '.qasm']
    
def construct_qiskit_clifford_circuit(num_qubits: int, num_circuits: int = 1, save_path: str = None, seed: int = None):
  """Generates a random clifford circuit using a random seed. If a save path is inputted, creates a .qasm file for the circuit, 
     containing the seed and number of qubits.
   
  Parameters:
    num_qubits (int): Required. Number of qubits for the circuit.
    num_circuits (int): Number of circuits to generate. (Default: 1)
    save_path (str): Path to save the random circuit to. (Default: None)
    seed (int): Manual seed for the quantum circuit. If no seed is inputted, one will be generated. (Default: None)
    
  Returns:
    If num_circuits is more than 1, returns a list of lists of random Clifford QuantumCircuits num_circuits long. 
    Otherwise, returns a list containing a random Clifford QuantumCircuit and its name.
  """
  if platform.system() == 'Windows' and save_path is not None:
    save_path = save_path.replace('\\', '/')
  qc_list = []
  for i in range(num_circuits):
    if seed == None:
      rand_seed = random.randint(10000, 99999)
    else:
      rand_seed = seed
    qc = random_clifford_circuit(num_qubits=num_qubits, seed=rand_seed)
    if isinstance(save_path,str) and os.path.isdir(save_path):
      dump(qc, save_path + '/qiskit_clifford_' + str(num_qubits) + '_' + str(rand_seed) + '.qasm')
    qc_list.append([qc,'qiskit_clifford_' + str(num_qubits) + '_' + str(rand_seed) + '.qasm' ])
  if num_circuits > 1:
    return qc_list
  else:
    return qc_list[0]

def construct_qiskit_bv_all_ones(num_qubits: int, save_path: str = None):
  """Generates a BV circuit over num_qubits for an all-ones bit string.
    If a save path is inputted, creates a .qasm file for the circuit, containing the seed, number of gates, and number of qubits.
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
        
    Returns:
        If num_circuits is more than 1, returns a list of lists of bv_all_ones QuantumCircuits and their names num_circuits long. 
        Otherwise, returns list containing a bv_all_ones QuantumCircuit and its name.
    """
  if platform.system() == 'Windows' and save_path is not None:
    save_path = save_path.replace('\\', '/')  
  qc_list = []
  
  qc = bv_all_ones(N=num_qubits)
  if isinstance(save_path,str) and os.path.isdir(save_path):
    dump(qc, f'{save_path}/qiskit_bv_all_ones_{str(num_qubits)}.qasm')
  qc_list.append([qc, f'qiskit_bv_all_ones_{str(num_qubits)}.qasm'])
  return qc_list
  
def construct_qiskit_clifford_optimized(num_qubits: int, num_circuits: int = 1, save_path: str = None, seed: int = None):
  """Generates a BV circuit over num_qubits for an all-ones bit string.
    If a save path is inputted, creates a .qasm file for the circuit, containing the seed, number of gates, and number of qubits.
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
        seed (int): Manual seed for the quantum circuit. If no seed is inputted, one will be generated. (Default: None)
        
    Returns:
        If num_circuits is more than 1, returns a list of lists of random optimized clifford QuantumCircuits and their names num_circuits long. 
        Otherwise, returns list containing a random optimized clifford QuantumCircuit and its name.
    """
  if platform.system() == 'Windows' and save_path is not None:
    save_path = save_path.replace('\\', '/')
  qc_list = []
  for i in range(num_circuits):
    if seed == None:
      rand_seed = random.randint(10000, 99999)
    else:
      rand_seed = seed
    qc = random_clifford_optimized(num_qubits=num_qubits, seed=rand_seed)
    if isinstance(save_path,str) and os.path.isdir(save_path):
      dump(qc, f'{save_path}/qiskit_random_clifford_optimized_{str(num_qubits)}_{rand_seed}.qasm')
    qc_list.append([qc, f'qiskit_random_clifford_optimized_{str(num_qubits)}_{rand_seed}.qasm'])
  if num_circuits > 1:
    return qc_list
  else:
    return qc_list[0]