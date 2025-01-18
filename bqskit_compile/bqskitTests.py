from bqskit.passes import (
    LEAPSynthesisPass,
    QSearchSynthesisPass,
    ForEachBlockPass,
    ScanPartitioner,
    QuickPartitioner,
    UnfoldPass
)
from bqskit.compiler import Compiler
from bqskit.ir import Circuit
import time
from bqskit_compile.partitioner import analyzePartitions

# NEED TO TRY CATCH FOR JSON SAVING.

# List of partitioners and partition size. Dictionary of partitioners to help with file nomenclature.
blockSize = 3
partitionerDict = {
        0: f'ScanPartitioner{blockSize}',
        1: f'QuckPartitioner{blockSize}'
    }
passDict = {
    0: 'QSearch',
    1: 'LEAP'
}
partitionerList = [ScanPartitioner(block_size=blockSize), QuickPartitioner(block_size=blockSize)]


def optimizationAnalysis(qc: str, save_path: str = None, success_threshold: float = 1e-8, replace_filter: str = 'less-than-multi', 
    partitioner: int = 0, pass_type: int = 0):
    """
    Optimizes a function using either LEAP or QSearch and returns the optimized circuit.

    Parameters:
        qc (str): Quantum circuit to be optimized. Path directory to QASM file.

        save_path (str): Path to save quantum circuits to. (Default: None)

        success_threshold (float): The distance threshold that determines successful termintation. (Default: 1e-8).

        replace_filter (str): A predicate that determines if the resulting circuit, after calling loop_body on a block, 
        should replace the original operation. (Default: less-than-multi).

        partitioner (int): Partitions circuit into blocks of 3 qubits. Supports ScanPartitioner and QuickPartitioner. 0 for
        ScanPartitioner and 1 for QuickPartitioner. (Default: 0).

        pass_type (int): Optimization algorithm to use. Supports QSearch and LEAP. 0 for QSearch, 1 for LEAP. (Default: 0).

    Returns:
        Optimized circuit saved to the save_path and a dictionary containing information about the optimization process.
    """

    #try to construct circuit for pre-optimization evaluation
    try:
        quantumCircuit = Circuit.from_file(qc)
    except:
        raise FileNotFoundError('Path is invalid.')
    
    # Time before compiling circuit
    sTime = time.time()

    # Compile circuit, with unfolded partitions to be able to see the compsition of each partition
    data = analyzePartitions(qc=qc, 
                                partitioner=partitioner, 
                                pass_type=pass_type, 
                                save_path=save_path, 
                                success_threshold=success_threshold,
                                replace_filter=replace_filter)
    circuit = data[0]
        
    # Time after compiling circuit
    eTime = time.time() 
        
    compiled_two_q_gates = 0
    original_two_q_gates = 0

    # Number of 2-qubit gates before compilation
    for gate in quantumCircuit.gate_counts:
        if gate.num_qudits == 1:
            continue
        original_two_q_gates += int(quantumCircuit.count(gate))

    # Number of 2-qubit gates after compilation
    for gate in circuit.gate_counts:
        if gate.num_qudits == 1:
            continue
        compiled_two_q_gates += int(circuit.count(gate))

    # 2-qubit depth after compilation
    compiled_two_q_depth = circuit.multi_qudit_depth

    # 2-qubit depth before compilation
    original_two_q_depth = quantumCircuit.multi_qudit_depth
        
    # time taken to compile
    elapsedTime = eTime - sTime

    # Circuit name before optimization
    index = qc.rfind('/')
    quantumCircuit_name = qc[index+1:len(qc)-5]

    # Circuit name after optimization 
    circuit_name = data[1].replace('.qasm', '')

    # Number of qubits in the circuit
    qc_qubit_count = circuit.num_qudits

    # Gate set before compilation
    gates = list(quantumCircuit.gate_set)
    before_qc_gate_set = ''
    for i in range(len(gates)- 1):
        before_qc_gate_set += str(gates[i]) + ', '
    before_qc_gate_set += str(gates[len(gates)-1])


    # Gate set after compilation
    gates = list(circuit.gate_set)
    after_qc_gate_set = ''
    for j in range(len(gates)- 1):
        after_qc_gate_set += str(gates[j]) + ', '
    after_qc_gate_set += ' ' + str(gates[len(gates)-1])


    infoDict = {
        'Circuit QASM Name Before Optimization': quantumCircuit_name,
        'Circuit QASM Name After Optimization': circuit_name,
        'Circuit Qubit Count': qc_qubit_count,
        'Compilation Time (seconds)': elapsedTime,
        'Two-Qubit Gate Count Before Optimization': original_two_q_gates,
        'Two-Qubit Gate Count After Optimization': compiled_two_q_gates,
        'Two-Qubit Gate Depth Before Optimzation': original_two_q_depth,
        'Two-Qubit Gate Depth After Optimzation': compiled_two_q_depth,
        'Gate Set Before Optimization': before_qc_gate_set,
        'Gate Set After Optimization': after_qc_gate_set,
        'Partitioner': partitionerDict[partitioner],
        'Optimization Algorithm': passDict[pass_type],
        'Optimization Algorithm Success Threshold': success_threshold,
        'Optimization Algorithm Replace Filter': replace_filter,
        'Partitioner Block Size': blockSize
        }
        
    return infoDict 


# a function that will first creat benchmark circuit, and then optimize them using different predetermined schemes
