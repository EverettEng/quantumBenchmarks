from circuits.bqskit_circuits import (
    bqskit_QV,
    bqskit_circSU2,
    dtc_unitary,
    multi_control_circuit,
    bqskit_random_clifford,
)
import random
from bqskit.ext import bqskit_to_qiskit
from qiskit.qasm2 import dump
import time
from bqskit import compile 

bench_path = 'benchmark_circuit_folders'


def construct_bqskit_QV(num_qubits: int, depth: int, num_circuits: int):
    for i in range(num_circuits):
        rand_seed = random.randint(10000, 99999)
        qc = bqskit_QV(num_qubits=num_qubits, depth=depth, seed=rand_seed)
        qc = compile(qc) # pickling 
        qc.save(f'{bench_path}/bqskit/qv/qv_{str(num_qubits)}_{str(depth)}_{str(rand_seed)}.qasm')
    
def construct_bqskit_circSU2(num_qubits: int, num_reps: int):
    """Generates an efficient SU2 circuit with circular entanglement and using Ry and Rz 1Q-gates.
    Creates a .qasm file for the circuit, containing the number of reps and number of qubits. 
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        num_reps (int): Required. Number of repitions. 
    """
    qc = bqskit_circSU2(width=num_qubits, num_reps=num_reps)
    qc.save(f'{bench_path}/bqskit/su2/su2_{str(num_qubits)}_{str(num_reps)}.qasm')

def construct_bqskit_dtc_unitary(num_qubits: int, num_circuits: int):
    """Generates a random Floquet unitary circuit with a random seed and random rotation from [1,9.9999].
    Creates a .qasm file for the circuit, containing the seed, x-rotation and number of qubits.
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        num_circuits (int): Required. Number of circuits to generate. 
    """
    for i in range(num_circuits):
        rand_seed = random.randint(10000, 99999)
        rand_float = rand_seed / 10000
        qc = dtc_unitary(num_qubits=num_qubits, g=rand_float, seed=rand_seed)
        qc.save(f'{bench_path}/bqskit/dtc/dtc_{str(num_qubits)}_{str(rand_float)}_{str(rand_seed)}.qasm')


def construct_bqskit_multi_control_circuit(num_qubits: int):
    qc = multi_control_circuit(num_qubits=num_qubits)
    qc.unfold_all() # pickle
    qc.save(f'{bench_path}/bqskit/multi_control/multi_control_{str(num_qubits)}.qasm')

def construct_bqskit_random_clifford(num_qubits: int, num_circuits: int):
    """Generates a random Floquet unitary circuit with a random seed and random rotation from [1,9.9999].
    Creates a .qasm file for the circuit, containing the seed, number of gates, and number of qubits.
    Parameters:
        num_qubits (int): Required. Number of qubits for the circuit.
        num_circuits (int): Required. Number of circuits to generate. 
    """
    for i in range(num_circuits):
        rand_seed = random.randint(10000, 99999)
        qc = bqskit_random_clifford(num_qubits=num_qubits, seed=rand_seed)
        qc.save(f'{bench_path}/bqskit/clifford/clifford_{str(num_qubits)}_{str(rand_seed)}.qasm')
        
        
if __name__ == '__main__':
    # nums = [10, 20, 30, 40, 50, 75, 100]
    # start_time = time.time()
    # for num in nums:
    #     construct_bqskit_circSU2(num_qubits=num, num_reps=3)
    #     construct_bqskit_dtc_unitary(num_qubits=num, num_circuits=10)
    #     construct_bqskit_random_clifford(num_qubits=num, num_circuits=10)
    # print(f'Done. Time taken to generate all circuits: {time.time() - start_time} seconds')
    # construct_bqskit_QV(num_circuits=1, num_qubits=10, depth=15)
    # construct_bqskit_multi_control_circuit(num_qubits=10) 
    construct_bqskit_random_clifford(num_circuits=1, num_qubits=3)
    print('done')