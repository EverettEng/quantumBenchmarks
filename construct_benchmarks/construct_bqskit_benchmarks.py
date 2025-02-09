from circuits.bqskit_circuits import (
    bqskit_QV,
    bqskit_circSU2,
    dtc_unitary,
    multi_control_circuit,
    bqskit_random_clifford,
    bqskit_bv_all_ones
)
import random
from bqskit import compile 
import os
from bqskit.ir.gates import ControlledGate

def construct_bqskit_QV(num_qubits: int, depth: int = None, num_circuits: int = 1, save_path: str = None):
    """Generate random QV circuit(s). If a save path is inputted, creates a .qasm file for the circuit, containing the number of reps and number of qubits. 
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        depth (int): Mumber of QV layers. (Default: None)
        num_circuits (int): Number of circuits to be generated. (Default: 1)
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
        
    Returns:
        If num_circuits is more than 1, returns a list of lists of random QV Circuits and their names num_circuits long. 
        Otherwise, returns a list containing a random QV Circuit and its name.
    """
    
    qc_list = []
    for i in range(num_circuits):
        rand_seed = random.randint(10000, 99999)
        qc = bqskit_QV(num_qubits=num_qubits, depth=depth, seed=rand_seed)
        qc = compile(qc)
        if isinstance(save_path, str) and os.path.isdir(save_path):
            qc.save(f'{save_path}/bqskit_qv_{str(num_qubits)}_{str(depth)}_{str(rand_seed)}.qasm')
        qc_list.append([qc, f'bqskit_qv_{str(num_qubits)}_{str(depth)}_{str(rand_seed)}.qasm'])
    if num_circuits > 1:
        return qc_list
    else:
        return qc_list[0]
    
def construct_bqskit_circSU2(num_qubits: int, num_reps: int = 3, save_path: str = None):
    """Generates an efficient SU2 circuit with circular entanglement and using Ry and Rz 1Q-gates.
    If a save path is inputted, creates a .qasm file for the circuit, containing the number of reps and number of qubits. 
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        num_reps (int): Number of repitions. (Default: 3)
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
    
    Returns:
        A list containing the constructed SU2 Circuit and its name. 
    """
    qc = bqskit_circSU2(width=num_qubits, num_reps=num_reps)
    if isinstance(save_path,str) and os.path.isdir(save_path):
        qc.save(f'{save_path}/bqskit_su2_{str(num_qubits)}_{str(num_reps)}.qasm')
    return [qc, f'bqskit_su2_{str(num_qubits)}_{str(num_reps)}.qasm']

def construct_bqskit_dtc_unitary(num_qubits: int, num_circuits: int = 1, save_path: str = None):
    """Generates a random Floquet unitary circuit with a random seed and random rotation from [1,9.9999].
    If a save path is inputted, creates a .qasm file for the circuit, containing the seed, x-rotation and number of qubits.
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        num_circuits (int): Number of circuits to generate. (Default: 1)
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
        
    Returns: 
        If num_circuits is more than 1, returns a list of lists of random DTC Circuits and their names num_circuits long. 
        Otherwise, returns list containing a random DTC Circuit and its name.
    """
    
    qc_list = []
    for i in range(num_circuits):
        rand_seed = random.randint(10000, 99999)
        rand_float = rand_seed / 10000
        qc = dtc_unitary(num_qubits=num_qubits, g=rand_float, seed=rand_seed)
        if isinstance(save_path, str) and os.path.isdir(save_path):
            qc.save(f'{save_path}/bqskit_dtc_{str(num_qubits)}_{str(rand_float)}_{str(rand_seed)}.qasm')
        qc_list.append([qc, f'bqskit_dtc_{str(num_qubits)}_{str(rand_float)}_{str(rand_seed)}.qasm'])
    if num_circuits > 1:
        return qc_list
    else:
        return qc_list[0]

def construct_bqskit_multi_control_circuit(num_qubits: int, save_path: str = None):
    """Generates a multi control circuit with num_qubits. DO NOT USE. USE THE QISKIT ONE
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
        
    Returns: 
        List containing a multi control circuit with num_qubits and its name.
    """
    qc = multi_control_circuit(num_qubits=num_qubits)

    qc.unfold_all()
    if isinstance(save_path,str) and os.path.isdir(save_path):
        qc.save(f'{save_path}/bqskit_multi_control_{num_qubits}.qasm')
        
    return [qc, f'bqskit_multi_control_{str(num_qubits)}.qasm']

def construct_bqskit_random_clifford(num_qubits: int, num_circuits: int = 1, save_path: str = None):
    """Generates a random Floquet unitary circuit with a random seed and random rotation from [1,9.9999].
    If a save path is inputted, creates a .qasm file for the circuit, containing the seed, number of gates, and number of qubits.
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        num_circuits (int): Number of circuits to generate. (Default: 1)
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
        
    Returns:
        If num_circuits is more than 1, returns a list of lists of random Clifford Circuits and their names num_circuits long. 
        Otherwise, returns list containing a random Clifford Circuit and its name.
    """
    
    qc_list = []
    for i in range(num_circuits):
        rand_seed = random.randint(10000, 99999)
        qc = bqskit_random_clifford(num_qubits=num_qubits, seed=rand_seed)
        if isinstance(save_path,str) and os.path.isdir(save_path):
            qc.save(f'{save_path}/bqskit_clifford_{str(num_qubits)}_{str(rand_seed)}.qasm')
        qc_list.append([qc, f'bqskit_clifford_{str(num_qubits)}_{str(rand_seed)}.qasm'])
    if num_circuits > 1:
        return qc_list
    else:
        return qc_list[0]
        
def construct_bqskit_bv_all_ones(num_qubits: int, num_circuits: int = 1, save_path: str = None):
    """Generates a BV circuit over num_qubits for an all-ones bit string.
    If a save path is inputted, creates a .qasm file for the circuit, containing the seed, number of gates, and number of qubits.
    
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        save_path (str): Path to save the quantum circuit(s) to. (Default: None)
        
    Returns:
        If num_circuits is more than 1, returns a list of bv_all_ones Circuit num_circuits long. 
        Otherwise, returns list containing a v_all_ones Circuit and its name.
    """
    qc_list = []
    for i in range(num_circuits):
        qc = bqskit_bv_all_ones(num_qubits=num_qubits)
        if isinstance(save_path,str) and os.path.isdir(save_path):
            qc.save(f'{save_path}/bqskit_bv_all_ones_{str(num_qubits)}.qasm')
        qc_list.append([qc, f'bqskit_bv_all_ones_{str(num_qubits)}.qasm'])
    if num_circuits > 1:
        return qc_list
    else:
        return qc_list[0]