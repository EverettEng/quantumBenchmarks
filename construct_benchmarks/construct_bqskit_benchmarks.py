from circuits.bqskit_circuits import (
    bqskit_QV,
    bqskit_circSU2,
    dtc_unitary,
    multi_control_circuit,
    bqskit_random_clifford,
)
import random
from bqskit import compile 
import os

def construct_bqskit_QV(num_qubits: int, depth: int, num_circuits: int, save_path: str = None):
    """Generate random QV circuit(s). If a save path is inputted, creates a .qasm file for the circuit, containing the number of reps and number of qubits. 
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        num_reps (int): Required. Number of repitions. 
        num_circuits (int): Number of circuits to be generated. (Default: 1)
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
        
    Returns:
        List of random QV Circuit(s) num_circuits long.
    """
    
    qc_list = []
    for i in range(num_circuits):
        rand_seed = random.randint(10000, 99999)
        qc = bqskit_QV(num_qubits=num_qubits, depth=depth, seed=rand_seed)
        qc = compile(qc)
        if isinstance(save_path, str) and os.path.isdir(save_path):
            qc.save(f'{save_path}/qv_{str(num_qubits)}_{str(depth)}_{str(rand_seed)}.qasm')
        qc_list.append(qc)
    return qc_list
    
def construct_bqskit_circSU2(num_qubits: int, num_reps: int, save_path: str = None):
    """Generates an efficient SU2 circuit with circular entanglement and using Ry and Rz 1Q-gates.
    If a save path is inputted, creates a .qasm file for the circuit, containing the number of reps and number of qubits. 
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        num_reps (int): Required. Number of repitions. 
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
    
    Returns:
        Constructed SU2 Circuit. 
    """
    qc = bqskit_circSU2(width=num_qubits, num_reps=num_reps)
    qc.save(f'{save_path}/su2_{str(num_qubits)}_{str(num_reps)}.qasm')
    return qc

def construct_bqskit_dtc_unitary(num_qubits: int, num_circuits: int = 1, save_path: str = None):
    """Generates a random Floquet unitary circuit with a random seed and random rotation from [1,9.9999].
    If a save path is inputted, creates a .qasm file for the circuit, containing the seed, x-rotation and number of qubits.
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        num_circuits (int): Number of circuits to generate. (Default: 1)
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
        
    Returns: 
        List of random QV Circuit(s) num_circuits long.
    """
    
    qc_list = []
    for i in range(num_circuits):
        rand_seed = random.randint(10000, 99999)
        rand_float = rand_seed / 10000
        qc = dtc_unitary(num_qubits=num_qubits, g=rand_float, seed=rand_seed)
        if isinstance(qc, str) and os.path.isdir(qc):
            qc.save(f'{save_path}/dtc_{str(num_qubits)}_{str(rand_float)}_{str(rand_seed)}.qasm')
        qc_list.append(qc)
    return qc_list


def construct_bqskit_multi_control_circuit(num_qubits: int, save_path: str = None):
    qc = multi_control_circuit(num_qubits=num_qubits)
    qc.unfold_all() # pickle
    qc.save(f'{save_path}/multi_control_{str(num_qubits)}.qasm')

def construct_bqskit_random_clifford(num_qubits: int, num_circuits: int = 1, save_path: str = None):
    """Generates a random Floquet unitary circuit with a random seed and random rotation from [1,9.9999].
    If a save path is inputted, creates a .qasm file for the circuit, containing the seed, number of gates, and number of qubits.
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        num_circuits (int): Required. Number of circuits to generate. 
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
        
    Returns:
        List of random Clifford Circuit(s) num_circuits long.
    """
    
    qc_list = []
    for i in range(num_circuits):
        rand_seed = random.randint(10000, 99999)
        qc = bqskit_random_clifford(num_qubits=num_qubits, seed=rand_seed)
        if isinstance(qc,str) and os.path.isdir(qc):
            qc.save(f'{save_path}/clifford_{str(num_qubits)}_{str(rand_seed)}.qasm')
        qc_list.append(qc)
    return qc_list
        