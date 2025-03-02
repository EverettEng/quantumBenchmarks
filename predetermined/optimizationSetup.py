from bqskit.passes import QSearchSynthesisPass, LEAPSynthesisPass, ScanPartitioner, QuickPartitioner, UnfoldPass
from bqskit_comp.partitioner import presetPartitions
import json
import os
from bqskit.ir import Circuit
from bqskit.compiler import Compiler
from qiskit.compiler import transpile
from qiskit import QuantumCircuit
import time
from qiskit.qasm2 import dump
from bqskit_comp.partitioner import countNumGates
from bqskit.ext import bqskit_to_qiskit, qiskit_to_bqskit
from qiskit.converters import circuit_to_dag, dag_to_circuit
from qiskit_ibm_runtime.fake_provider import FakeWashingtonV2, FakeTorino

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
replaceFilterType = 'less-than-multi'
success_threshold_num = 1e-8

optimizationLevel = 3
generated_circuit_name = ''
qiskit_circuit_name = ''

def optimizations(qc: str|Circuit|QuantumCircuit|list, replace_filter: str = 'always', save_path: str = None, success_threshold: float = 1e-8, partitioner: int = 0, 
                  generate_circuit: bool = False, circuit_name: str = None):
    """
        Helper function. Does the actual compilation. Do not call. Circuit name is used for randomly generated circuit
    """
    data = []
    compiled_circuits = []
    compiled_circuits_times = []
    
    # Stores these variables for the helper functions to use 
    global partitionerType, replaceFilterType, success_threshold_num, generated_circuit_name, qiskit_circuit_name
    partitionerType = partitioner
    replaceFilterType = replace_filter
    success_threshold_num = success_threshold
    generated_circuit_name = circuit_name

    
    # Runs if qc is a string (path)
    if not generate_circuit:
        
        # Optimizes the circuit using both LEAP and QSearch
        for i in range(2):
            #Start time of optimization
            
        
            if 'qiskit' in qc:
                circ1 = QuantumCircuit.from_qasm_file(qc)
                circ2 = transpile(circ1, optimization_level=0)
                circ = qiskit_to_bqskit(circ2)
            else:
                circ = Circuit.from_file(qc)
                
            index = qc.rfind('/')
            circuit_name = qc[index+1:len(qc)-5]
            startTime = time.time() 
            # Optimizes the circuit using the inputted parameters
            compiled_circuit = presetPartitions(qc=circ, 
                            pass_type=i,
                            partitioner=partitioner,
                            success_threshold=success_threshold,
                            save_path=save_path,
                            replace_filter=replace_filter,
                            circuit_name=circuit_name)
            # End time of optimization
            endTime = time.time()
            elapsedTime = endTime - startTime - compiled_circuit[-1]
            # Appends list of data which includes the compiled circuit to compiled_circuits (Indices 0 and 1).
            # Their respective compilation times are added to a separate list (Indices 0 and 1).
            compiled_circuits.append(compiled_circuit)
            compiled_circuits_times.append((elapsedTime))

        # Creates a QuantumCircuit object out of the qc path
        qiskit_circuit = QuantumCircuit.from_qasm_file(qc)

        # Start of transpilation
        startTime = time.time()
        # Optimizes the circuit using optimization level 3 (optimizationLevel)
        compiled_circuit = transpile(qiskit_circuit, optimization_level=optimizationLevel, basis_gates=['cx','rz','x','sx'])
        # End of transpilation
        endTime = time.time()
        compiled_circuit.remove_final_measurements()

        # Gets the name of the quantum circuit before compilation 
        index = qc.rfind('/')
        qiskit_circuit_name = qc[index+1:len(qc)-5]
        
        # Appends the compilation time (Index 2)
        compiled_circuits_times.append(endTime-startTime)
        # Appends list of data which includes the compiled circuit to compiled_circuits (Index 2).
        compiled_circuits.append([compiled_circuit, f'{qiskit_circuit_name}_OptimizationLevel{optimizationLevel}.qasm'])

        # If there is a valid save path the circuit is saved
        if isinstance(save_path,str) and os.path.isdir(save_path):
            dump(compiled_circuit, f'{save_path}/{qiskit_circuit_name}_OptimizationLevel{optimizationLevel}.qasm')

        # Runs analysis on the circuits
        presetBqskitOptimizationAnalysis(qc=qc, compiled_circuits=compiled_circuits, compiled_circuits_times=compiled_circuits_times, data=data)
        presetQiskitOptimizationAnalysis(qc=qc, compiled_circuits=compiled_circuits, compiled_circuits_times=compiled_circuits_times, data=data)  
    
    # Runs if the circuit is a randomly generated circuit 
    else:
        generated_circuit_name = circuit_name
        
        # Checks to see if the circuit inputted is a QuantumCircuit, if it is, converts it to a Circuit so that it can be compiled in. Specify which framework the circuits come from before optimzizaton
        # bqskit
        if isinstance(qc, QuantumCircuit):
            transpile(qc, optimization_level=0)
            qc = qiskit_to_bqskit(qc)
        
        # Decompose only using qiskit w/o any optimizations (level 0) and specify basic gates. Only qiskit ciruits
        # Optimizes the circuit using both LEAP and QSearch
        for i in range(2):
            # Start time of compilation
            startTime = time.time()
            # Optimizes the circuit using the inputted parameters
            
            compiled_circuit = presetPartitions(qc=qc, 
                            pass_type=i,
                            partitioner=partitioner,
                            success_threshold=success_threshold,
                            save_path=save_path,
                            replace_filter=replace_filter,
                            circuit_name=circuit_name)
            
            # End time of compilation
            endTime = time.time()
            
            # Appends list of data whcih includes the compiled circuit ti compiled_circuits (Indices 0 and 1).
            # Their respective compilation times are added to a separate list (Indices 0 and 1).
            compiled_circuits.append(compiled_circuit)
            compiled_circuits_times.append(endTime-startTime)
        
        # Checks to see if the circuit inputted is a Circuit, if it is, converts it to a QuantumCircuit so that it can be compiled in
        # qiskit
        if isinstance(qc, Circuit):
            qiskit_circuit = bqskit_to_qiskit(qc)
        else:
            qiskit_circuit = qc
            
        # Start time of transpilation
        startTime = time.time()
        compiled_circuit = transpile(qiskit_circuit, optimization_level=optimizationLevel, basis_gates=['x','sx','cx','rz'])     
        # End time of transpilation
        endTime = time.time()
        
        compiled_circuit.remove_final_measurements()

        # Gets the name of the circuit from the circuit_name parameter since the circuit is an object instead of a file
        quantumCircuit_name = circuit_name[:len(circuit_name)-5]

         # Appends the compilation time (Index 2)
        compiled_circuits_times.append(endTime-startTime)
        # Appends list of data which includes the transpiled circuit to compiled_circuits (Index 2).
        compiled_circuits.append([compiled_circuit, f'{quantumCircuit_name}_OptimizationLevel{optimizationLevel}.qasm'])
        
        # Saves the tranpiled circuit if there is a valid save path
        if isinstance(save_path,str) and os.path.isdir(save_path):
            dump(compiled_circuit, f'{save_path}/{quantumCircuit_name}_OptimizationLevel{optimizationLevel}.qasm')
        
        # Calls functions to collect data on the circuits
        presetBqskitOptimizationAnalysis(qc=qc, compiled_circuits=compiled_circuits, compiled_circuits_times=compiled_circuits_times, data=data)
        presetQiskitOptimizationAnalysis(qc=qiskit_circuit, compiled_circuits=compiled_circuits, compiled_circuits_times=compiled_circuits_times, data=data)  

    # Returns a list of dictionaries containing data on the compiled circuit
    
    return data


def presetBqskitOptimizationAnalysis(qc: str|Circuit, data: list, compiled_circuits_times: list, compiled_circuits: list):
    """
        Helper function. Do not call.
    """
    
    if isinstance(qc,str):
        quantumCircuit = Circuit.from_file(qc)
    else:
        quantumCircuit = qc   
    
    for i in range(2):
         
        circuiti = compiled_circuits[i][0]

        # Circuit name before optimization if the circuit is QASM file
        if isinstance(qc,str):
            index = qc.rfind('/')
            quantumCircuit_name = qc[index+1:len(qc)-5]
         # Circuit name before optimization if it is randomly generated
        else:
            quantumCircuit_name = generated_circuit_name[:len(generated_circuit_name)-5]

        # Circuit name after optimization 
        circuit_name = compiled_circuits[i][1].replace('.qasm', '')

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
        
        # Transpile so that there is only cx gates as the 2q gate type
        quantumCircuit = bqskit_to_qiskit(quantumCircuit)
        multi_qubit_gates = [instr.operation.name for instr in quantumCircuit.data if len(instr.qubits) > 1 and instr.operation.name != 'cx']

        multi_qubit_gates = list(set(multi_qubit_gates))
        basis_gates = []
        gates = list(quantumCircuit.count_ops())
        basis_gates = list(set(gates) - set(multi_qubit_gates))
        if 'cx' not in basis_gates:
            basis_gates.append('cx')
        quantumCircuit = transpile(quantumCircuit, basis_gates=basis_gates, optimization_level=0)
        quantumCircuit = qiskit_to_bqskit(quantumCircuit)
        
        original_two_q_gates = 0
        compiled_two_q_gates = 0
        
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

        infoDict = {
        'Circuit QASM File Name Before Optimization': quantumCircuit_name,
        'Circuit QASM File Name After Optimization': circuit_name,
        'Circuit Qubit Count': qc_qubit_count,
        'Compilation Time (seconds)': compiled_circuits_times[i] - compiled_circuits[i][6],
        'Two-Qubit Gate Count Before Optimization': original_two_q_gates,
        'Two-Qubit Gate Count After Optimization': compiled_two_q_gates,
        'Two-Qubit Gate Depth Before Optimization': original_two_q_depth,
        'Two-Qubit Gate Depth After Optimization': compiled_two_q_depth,
        'Gate Count Before Optimization': countNumGates(quantumCircuit),
        'Gate Count After Optimization': countNumGates(compiled_circuits[i][0]),
        'Gate Set Before Optimization': before_qc_gate_set,
        'Gate Set After Optimization': after_qc_gate_set,
        'Partitioner': partitionerDict[partitionerType],
        'Optimization Algorithm': passDict[i],
        'Optimization Algorithm Success Threshold': success_threshold_num,
        'Optimization Algorithm Replace Filter': replaceFilterType,
        'Partitioner Block Size': blockSize,
        'Multistart Value': '2^3',
        'Average Number of Gates in Each Partition Before Optimization': compiled_circuits[i][2],
        'Average Number of Gates in Each Partition After Optimization': compiled_circuits[i][3],
        'Average Number of Two-Qubit Gates in Each Partition Before Optimization': compiled_circuits[i][4],
        'Average Number of Two-Qubit Gates in Each Partition After Optimization': compiled_circuits[i][5],
        'Optimization Level': None,
        'Randomly Generated Circuit': True if isinstance(qc, Circuit) else False,
        'Framework': 'BQSkit'
        }
        
        data.append(infoDict)

def presetQiskitOptimizationAnalysis(qc: str|QuantumCircuit, data: list, compiled_circuits_times: list, compiled_circuits: list):
    """
        Helper function. Do not call.
    """
    # original circuit
    if isinstance(qc,str):
        quantumCircuit = QuantumCircuit.from_qasm_file(qc)
    else:
        quantumCircuit = qc


    # compiled circuit
    circuit = compiled_circuits[2][0]

    # Circuit name before optimization if it is a QASM file
    if isinstance(qc,str):
        quantumCircuit_name = qiskit_circuit_name
    # Circuit name before optimization if it is randomly generated
    else:
        quantumCircuit_name = generated_circuit_name[:len(generated_circuit_name)-5]

    # Circuit name after optimization 
    circuit_name = compiled_circuits[2][1][:-5]

    # Number of qubits in the circuit 
    qc_qubit_count = circuit.num_qubits
    
    # Number of gates before optimization
    gate_counts = quantumCircuit.count_ops()
    gate_count_before_optimization = sum(gate_counts.values())
    
    # Number of gates after optimization
    gate_counts = circuit.count_ops()
    gate_count_after_optimization = sum(gate_counts.values())

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
    
    original_two_q_gates = 0
    compiled_two_q_gates = 0
    
    # Number of 2-qubit gates before compilation
    # Transpile so that there is only cx gates as the 2q gate type
    multi_qubit_gates = [gate.name for gate, qubits, _ in quantumCircuit.data if len(qubits) > 1 and gate.name != 'cx']
    basis_gates = list(set(before_qc_gate_set) - set(multi_qubit_gates))
    if 'cx' not in basis_gates:
        basis_gates.append('cx')
    quantumCircuit = transpile(quantumCircuit, basis_gates=basis_gates, optimization_level=0)

    for instruction in quantumCircuit.data:
        qubits = instruction.qubits
        if len(qubits) > 1:
            original_two_q_gates += 1

    # Number of 2-qubit gates after compilation
    for instruction in circuit.data:
        qubits = instruction.qubits
        if len(qubits) > 1:
            compiled_two_q_gates += 1
    
    # Two qubit gate depth before optimization
    two_q_gate_depth_before_optimization = qiskit_to_bqskit(quantumCircuit).multi_qudit_depth
    
    # Two qubit gate depth after optimization
    two_q_gate_depth_after_optimization = qiskit_to_bqskit(circuit).multi_qudit_depth
    
    infoDict = {
        'Circuit QASM File Name Before Optimization': quantumCircuit_name,
        'Circuit QASM File Name After Optimization': circuit_name,
        'Circuit Qubit Count': qc_qubit_count,
        'Compilation Time (seconds)': compiled_circuits_times[2],
        'Two-Qubit Gate Count Before Optimization': original_two_q_gates,
        'Two-Qubit Gate Count After Optimization': compiled_two_q_gates,
        'Two-Qubit Gate Depth Before Optimization': two_q_gate_depth_before_optimization,
        'Two-Qubit Gate Depth After Optimization': two_q_gate_depth_after_optimization,
        'Gate Count Before Optimization': gate_count_before_optimization,
        'Gate Count After Optimization': gate_count_after_optimization,
        'Gate Set Before Optimization': before_qc_gate_set,
        'Gate Set After Optimization': after_qc_gate_set,
        'Partitioner': None,
        'Optimization Algorithm': None,
        'Optimization Algorithm Success Threshold': None,
        'Optimization Algorithm Replace Filter': None,
        'Partitioner Block Size': None,
        'Multistart Value': None,
        'Average Number of Gates in Each Partition Before Optimization': None,
        'Average Number of Gates in Each Partition After Optimization': None,
        'Average Number of Two-Qubit Gates in Each Partition Before Optimization': None,
        'Average Number of Two-Qubit Gates in Each Partition After Optimization': None,
        'Optimization Level': optimizationLevel,
        'Randomly Generated Circuit': False if isinstance(qc,str) else True,
        'Framework': 'Qiskit'
        }
        
    data.append(infoDict)