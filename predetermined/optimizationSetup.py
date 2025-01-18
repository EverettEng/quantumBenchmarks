from bqskit.passes import QSearchSynthesisPass, LEAPSynthesisPass, ScanPartitioner, QuickPartitioner, UnfoldPass
from bqskit_compile.partitioner import presetPartitions
import json
import os
from bqskit.ir import Circuit
from bqskit.compiler import Compiler
from qiskit.compiler import transpile
from qiskit import QuantumCircuit
import time
from qiskit.qasm2 import dump

compiled_circuits = []
compiled_circuits_times = []
blockSize = 3
partitionerDict = {
        0: f'ScanPartitioner{blockSize}',
        1: f'QuckPartitioner{blockSize}'
    }
partitionerType = 0
passDict = {
    0: 'QSearch',
    1: 'LEAP'
}
replaceFilterType = 0
success_threshold_num = 0
data = []

def optimizations(qc: str, save_path: str = None, success_threshold: float = 1e-8, replace_filter: str = 'less-than-multi', 
    partitioner: int = 0):

    partitionerType = partitioner
    replaceFilterType = replace_filter
    success_threshold_num = success_threshold

    for i in range(2):
        startTime = time.time()
        compiled_circuit = presetPartitions(qc=qc, 
                         pass_type=i,
                         partitioner=partitioner,
                         success_threshold=success_threshold,
                         save_path=save_path,
                         replace_filter=replace_filter)
        endTime = time.time()
        compiled_circuits.append(compiled_circuit)
        compiled_circuits_times.append(endTime-startTime)

    qiskit_circuit = QuantumCircuit.from_qasm_file(qc)

    startTime = time.time()
    compiled_circuit = transpile(qiskit_circuit, optimization_level=3)
    endTime = time.time()

    index = qc.rfind('/')
    quantumCircuit_name = qc[index+1:len(qc)-5]

    compiled_circuits_times.append(endTime-startTime)
    compiled_circuits.append([compiled_circuit, quantumCircuit_name])

    
    dump(compiled_circuit, f'{save_path}/{quantumCircuit_name}_OptimizationLevel3.qasm')

    presetBqskitOptimizationAnalysis(qc=qc)
    presetQiskitOptimizationAnalysis(qc=qc)

    return data


def presetBqskitOptimizationAnalysis(qc: str):

    for i in range(2):
        quantumCircuit = Circuit.from_file(qc)

        original_two_q_gates = 0
        compiled_two_q_gates = 0

        circuiti = compiled_circuits[i][0]

        # Number of 2-qubit gates before compilation
        for gate in quantumCircuit.gate_counts:
            if gate.num_qudits == 1:
                continue
            original_two_q_gates += int(quantumCircuit.count(gate))

        # Number of 2-qubit gates after compilation
        for gate in circuiti.gate_counts:
            if gate.num_qudits == 1:
                continue
            compiled_two_q_gates += int(circuiti.count(gate))

        # 2-qubit depth after compilation
        compiled_two_q_depth = circuiti.multi_qudit_depth

        # 2-qubit depth before compilation
        original_two_q_depth = quantumCircuit.multi_qudit_depth

        # Circuit name before optimization
        index = qc.rfind('/')
        quantumCircuit_name = qc[index+1:len(qc)-5]

        # Circuit name after optimization 
        circuit_name = compiled_circuits[i][1]

        # Number of qubits in the circuit 
        qc_qubit_count = circuiti.num_qudits

        # Gate set before compilation
        gates = list(quantumCircuit.gate_set)
        before_qc_gate_set = ''
        for j in range(len(gates)- 1):
            before_qc_gate_set += str(gates[j]) + ', '
        before_qc_gate_set += str(gates[len(gates)-1])


        # Gate set after compilation
        gates = list(circuiti.gate_set)
        after_qc_gate_set = ''
        for k in range(len(gates)- 1):
            after_qc_gate_set += str(gates[k]) + ', '
        after_qc_gate_set += ' ' + str(gates[len(gates)-1])

        infoDict = {
        'Circuit QASM Name Before Optimization': quantumCircuit_name,
        'Circuit QASM Name After Optimization': circuit_name,
        'Circuit Qubit Count': qc_qubit_count,
        'Compilation Time (seconds)': compiled_circuits_times[i],
        'Two-Qubit Gate Count Before Optimization': original_two_q_gates,
        'Two-Qubit Gate Count After Optimization': compiled_two_q_gates,
        'Two-Qubit Gate Depth Before Optimzation': original_two_q_depth,
        'Two-Qubit Gate Depth After Optimzation': compiled_two_q_depth,
        'Gate Set Before Optimization': before_qc_gate_set,
        'Gate Set After Optimization': after_qc_gate_set,
        'Partitioner': partitionerDict[partitionerType],
        'Optimization Algorithm': passDict[i],
        'Optimization Algorithm Success Threshold': success_threshold_num,
        'Optimization Algorithm Replace Filter': replaceFilterType,
        'Partitioner Block Size': blockSize,
        'Multistart value': '2^3',
        'Framework': 'BQSkit'
        }
        
        data.append(infoDict)

def presetQiskitOptimizationAnalysis(qc):
    
    # original circuit
    quantumCircuit = QuantumCircuit.from_qasm_file(qc)

    original_two_q_gates = 0
    compiled_two_q_gates = 0

    # compiled circuit
    circuit = compiled_circuits[2][0]

    # Number of 2-qubit gates before compilation
    for instruction in quantumCircuit.data:
        qubits = instruction.qubits
        if len(qubits) == 2:
            original_two_q_gates += 1

    # Number of 2-qubit gates after compilation
    for instruction in circuit.data:
        qubits = instruction.qubits
        if len(qubits) == 2:
            compiled_two_q_gates += 1

     # 2-qubit depth after compilation. Need to figure out
    compiled_two_q_depth = 0

    # 2-qubit depth before compilation. Need to figure out
    original_two_q_depth = 0

    # Circuit name before optimization
    index = qc.rfind('/')
    quantumCircuit_name = qc[index+1:len(qc)-5]

    # Circuit name after optimization 
    circuit_name = compiled_circuits[2][1]

    # Number of qubits in the circuit 
    qc_qubit_count = circuit.num_qubits

    # Gate set before compilation
    gates = list(quantumCircuit.count_ops())
    before_qc_gate_set = ''
    for i in range(len(gates)-1):
        before_qc_gate_set += gates[i] + ', '
    before_qc_gate_set += gates[len(gates)-1]
        

    # Gate set after compilation
    gates = list(circuit.count_ops())
    after_qc_gate_set = ''
    for i in range(len(gates)-1):
        after_qc_gate_set += gates[i] + ', '
    after_qc_gate_set += gates[len(gates)-1]

    infoDict = {
        'Circuit QASM Name Before Optimization': quantumCircuit_name,
        'Circuit QASM Name After Optimization': circuit_name,
        'Circuit Qubit Count': qc_qubit_count,
        'Compilation Time (seconds)': compiled_circuits_times[2],
        'Two-Qubit Gate Count Before Optimization': original_two_q_gates,
        'Two-Qubit Gate Count After Optimization': compiled_two_q_gates,
        'Two-Qubit Gate Depth Before Optimzation': original_two_q_depth,
        'Two-Qubit Gate Depth After Optimzation': compiled_two_q_depth,
        'Gate Set Before Optimization': before_qc_gate_set,
        'Gate Set After Optimization': after_qc_gate_set,
        'Framework': 'Qiskit'
        }
        
    data.append(infoDict)        