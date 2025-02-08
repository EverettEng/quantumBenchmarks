from bqskit.compiler import Compiler, MachineModel, GateSet
from bqskit.ir import Circuit, Gate
from bqskit.ir.gates import RZGate, CNOTGate, XGate, SqrtXGate
from bqskit.passes import (QSearchSynthesisPass, 
                           QuickPartitioner,
                           UnfoldPass, 
                           LEAPSynthesisPass, 
                           ScanPartitioner, 
                           SetModelPass, 
                           ZXZXZDecomposition,
                           IfThenElsePass, 
                           PassPredicate,
                           HasGeneralSingleQuditGate,
                           ForEachBlockPass,
                           ManyQuditGatesPredicate,
                           NotPredicate,
                           NoSingleQuditGatesInModel)
import os
from bqskit.ir.gates import MeasurementPlaceholder, BarrierPlaceholder
import time
from qiskit import transpile, QuantumCircuit
from bqskit.ext import qiskit_to_bqskit, bqskit_to_qiskit


blockSize = 3
partitionerDict = {
        0: f'ScanPartitioner{blockSize}',
        1: f'QuckPartitioner{blockSize}'
    }
passDict = {
    0: 'QSearch',
    1: 'LEAP'
}


def countNumGates(circuit):
    num = 0
    for gate in circuit.gate_counts:
        num += int(circuit.count(gate))
    return num

def countTwoQGates(circuit):
    num = 0
    for gate in circuit.gate_counts:
        if gate.num_qudits == 1:
            continue
        num += int(circuit.count(gate))
    return num

def analyzePartitions(qc: str, pass_type: int, partitioner: int, success_threshold: float, save_path: str, replace_filter: str):
    """
    Replicates ForEachBlockPass 

    Parameters:
        qc (str): Quantum circuit to be optimized. Path directory to QASM file.

        pass_type (int): Optimization algorithm to use. Supports QSearch and LEAP. 0 for QSearch, 1 for LEAP. (Default: 0).

        partitioner (int): Partitions circuit into blocks of 3 qubits. Supports ScanPartitioner and QuickPartitioner. 0 for
        ScanPartitioner and 1 for QuickPartitioner. (Default: 0).

        success_threshold (float): The distance threshold that determines successful termintation. (Default: 1e-8).

        save_path (str): The fie path to save the string to. (Default: None).

        replace_filter (str): A predicate that determines if the resulting circuit, after calling loop_body on a block, 
        should replace the original operation. (Default: 'always'). Support for 'less-than', 'always', and 'less-than-multi'. 


    Returns:
        Optimized circuit, the name of the circuit, the number of gates in each partition before optimization, the number of gates
        in each partition after optimization, the number of 2-qubit gates in each partition before optimization, and the number of 
        two-qubit gates in each partition after optimization. If there is a valid save_path, saves compiled circuit to save_path.
        Sets basis gates to CX, RZ, SX, X, and Measure
    """

    # Instantiate compiler and get the file
    compiler = Compiler()
    circuit = Circuit.from_file(filename=qc)
    
    passes = [QSearchSynthesisPass(success_threshold=success_threshold), 
            LEAPSynthesisPass(success_threshold=success_threshold)]

    partitioners = [ScanPartitioner(block_size=blockSize), 
                    QuickPartitioner(block_size=blockSize)]

    # Unfolds all gates
    circuit.unfold_all()
    circuit.remove_all_measurements()

    # Compiles using the partitioner selected
    out = compiler.compile(circuit, partitioners[partitioner])
    
    # Workflow
    optimization_workflow = [passes[pass_type], UnfoldPass()]

    # Ids of submitted sub-circuits
    ids = []

    # Respective locations in the original circuit
    locations = []

    partitionList = []
    # Iterates over each partition of the compiled circuit (out)
    for partition in out:
        # Appends the location of the partition in the original circuit to the locations list
        locations.append(partition.location)

        # Creates a sub_circuit from the partition
        sub_circ = Circuit.from_operation(partition)

        # Unfolds gates in sub_circ
        sub_circ.unfold_all()
        partitionList.append(sub_circ)

        # Submits a compilation task using the workflow above to the compiler. Returns an ID that represents the completed task
        id = compiler.submit(sub_circ, optimization_workflow)

        # appends the ID of the compilation task to the ID list, allowing for the tracking of the partition optimizations 
        ids.append(id)


    # Checks the status of all submitted circuits, waiting until they are all compiled (status 2)
    #while all(compiler.status(id) != 2 for id in ids):
    #    continue

    # New circuit is instantiated to hold the final optimized circuits, initialized with the same amount of qudits as the original circuit
    final_circuit = Circuit(num_qudits=circuit.num_qudits)

    # List of the optimized subcircuits
    optimized_subcircuit = []
    partitionList = []
    numGatesBeforeOptimization = []
    numGatesAfterOptimization = []
    numTwoQGatesBeforeOptimizatoon = []
    numTwoQGatesAfterOptimization = []

    
    for id, loc, originalSubcirc in zip(ids, locations, partitionList):
        
        if (replace_filter == 'always'):
            replace_filter_condition_met = True
        # retrieves the result by calling the compiled partition's ID
        sub_circ = compiler.result(id)
        numGatesBeforeOptimization.append(countNumGates(originalSubcirc))
        numGatesAfterOptimization.append(countNumGates(sub_circ))
        numTwoQGatesBeforeOptimizatoon.append(countTwoQGates(originalSubcirc))
        numTwoQGatesAfterOptimization.append(countTwoQGates(sub_circ))

        if replace_filter == 'less-than':
            replace_filter_condition_met = countNumGates(originalSubcirc) > countNumGates(sub_circ)
        if replace_filter == 'less-than-multi':
            replace_filter_condition_met = countTwoQGates(originalSubcirc) > countTwoQGates(sub_circ)
    
    
        if replace_filter_condition_met:
            # adds the unfolded optimized partition to the optimized_subcircuit list 
            optimized_subcircuit.append(sub_circ.unfold_all())
            # Merge sub_circ (the optimized partition) into the finalized circuit. Loc specifies where to append sub_circ to (which qubits)
            final_circuit.append_circuit(sub_circ, loc)
        else:
            # adds the unfolded original partition to the optimized_subcircuit list 
            optimized_subcircuit.append(originalSubcirc.unfold_all())
            # Merge originalSubCirq (the original partition) into the finalized circuit. Loc specifies where to append sub_circ to (which qubits)
            final_circuit.append_circuit(originalSubcirc, loc)

    final_circuit.unfold_all() # unfold any circuit gates
    
    final_circuit = bqskit_to_qiskit(final_circuit)
    
    final_circuit = transpile(final_circuit, optimization_level=0, basis_gates=['x','sx','rz','cx'])
    final_circuit = qiskit_to_bqskit(final_circuit)
    final_circuit.unfold_all()

    compiler.close()
    # Start time of the stuff after compilation
    sTime = time.time()
    # get the name of the QASM file without the .qasm
    index = qc.rfind('/')
    file_name = qc[index+1:len(qc)-5]

    # Save circuit
    if isinstance(save_path,str):
        final_circuit.save(f'{save_path}/{file_name}_{success_threshold}_{partitionerDict[partitioner]}_{passDict[pass_type]}.qasm')
        
    # End time of the stuff after compilation
    eTime = time.time()
    
    # Return optimized circuit, the name of the circuit, the number of gates in each partition before optimization, the number of gates
    # in each partition after optimization, the number of 2-qubit gates in each partition before optimization, the extra time taken
    # to save the circuit and the number of two-qubit gates in each partition after optimization.
    return [final_circuit, 
            f'{file_name}_{success_threshold}_{partitionerDict[partitioner]}_{passDict[pass_type]}.qasm', 
            sum(numGatesBeforeOptimization)/len(numGatesBeforeOptimization),
            sum(numGatesAfterOptimization)/len(numGatesAfterOptimization),
            sum(numTwoQGatesBeforeOptimizatoon)/len(numTwoQGatesBeforeOptimizatoon),
            sum(numTwoQGatesAfterOptimization)/len(numTwoQGatesAfterOptimization),
            eTime-sTime]

def presetPartitions(qc: str|Circuit, pass_type: int, partitioner: int, success_threshold: float, save_path: str, replace_filter: str, circuit_name: str = None):
    """
    Replicates ForEachBlockPass with preset partitions

    Parameters:
        qc (str): Quantum circuit to be optimized. Path directory to QASM file.

        pass_type (int): Optimization algorithm to use. Supports QSearch and LEAP. 0 for QSearch, 1 for LEAP. (Default: 0).

        partitioner (int): Partitions circuit into blocks of 3 qubits. Supports ScanPartitioner and QuickPartitioner. 0 for
        ScanPartitioner and 1 for QuickPartitioner. (Default: 0).

        success_threshold (float): The distance threshold that determines successful termintation. (Default: 1e-8).

        save_path (str): The fie path to save the string to. (Default: None).

        replace_filter (str): A predicate that determines if the resulting circuit, after calling loop_body on a block, 
        should replace the original operation. (Default: 'always'). Support for 'less-than', 'always', and 'less-than-multi'. 


    Returns:
        Optimized circuit saved to the save_path and a dictionary containing information about the optimization process.
    """    
    

    # Instantiate compiler and get the file
    compiler = Compiler()
    if isinstance(qc,str):
        circuit = Circuit.from_file(filename=qc)
    else:
        circuit = qc

    # Unfolds all gates
    circuit.unfold_all()
    circuit.remove_all_measurements()

    # Gate set to use

    passes = [QSearchSynthesisPass(success_threshold=success_threshold, instantiate_options={'multistart': 2 ** 3}), 
            LEAPSynthesisPass(success_threshold=success_threshold, instantiate_options={'multistart': 2 ** 3})]

    partitioners = [ScanPartitioner(block_size=blockSize), 
                    QuickPartitioner(block_size=blockSize)]
    
    # Compiles using the partitioner selected
    out = compiler.compile(circuit, partitioners[partitioner])
    
    # Workflow
    optimization_workflow = [passes[pass_type], UnfoldPass()]

    # Ids of submitted sub-circuits
    ids = []

    # Respective locations in the original circuit
    locations = []

    # Iterates over each partition of the compiled circuit (out)
    partitionList = []
    
    # for clifford_10_98001 there is 183 partitions
    for partition in out:
        # Appends the location of the partition in the original circuit to the locations list
        locations.append(partition.location)

        # Creates a sub_circuit from the partition
        sub_circ = Circuit.from_operation(partition)

        # Unfolds gates in sub_circ
        sub_circ.unfold_all()
        partitionList.append(sub_circ)

        # Submits a compilation task using the workflow above to the compiler. Returns an ID that represents the completed task
        id = compiler.submit(sub_circ, optimization_workflow)

        # appends the ID of the compilation task to the ID list, allowing for the tracking of the partition optimizations 
        ids.append(id)


    # Checks the status of all submitted circuits, waiting until they are all compiled (status 2)
    #while all(compiler.status(id) != 2 for id in ids):
    #    continue

    # New circuit is instantiated to hold the final optimized circuits, initialized with the same amount of qudits as the original circuit
    final_circuit = Circuit(num_qudits=circuit.num_qudits)

    # List of the optimized subcircuits
    optimized_subcircuit = []
    
    numGatesBeforeOptimization = []
    numGatesAfterOptimization = []
    numTwoQGatesBeforeOptimizatoon = []
    numTwoQGatesAfterOptimization = []

    for id, loc, originalSubcirc in zip(ids, locations, partitionList):
        replace_filter_condition_met = True
        # retrieves the result by calling the compiled partition's ID
        sub_circ = compiler.result(id)

        numGatesBeforeOptimization.append(countNumGates(originalSubcirc))
        numGatesAfterOptimization.append(countNumGates(sub_circ))
        numTwoQGatesBeforeOptimizatoon.append(countTwoQGates(originalSubcirc))
        numTwoQGatesAfterOptimization.append(countTwoQGates(sub_circ))
        
        
        if replace_filter == 'less-than':
            replace_filter_condition_met = countNumGates(originalSubcirc) > countNumGates(sub_circ)
        if replace_filter == 'less-than-multi':
            replace_filter_condition_met = countTwoQGates(originalSubcirc) > countTwoQGates(sub_circ)
        
        
        if replace_filter_condition_met:
            # adds the unfolded optimized partition to the optimized_subcircuit list 
            optimized_subcircuit.append(sub_circ.unfold_all())
            # Merge sub_circ (the optimized partition) into the finalized circuit. Loc specifies where to append sub_circ to (which qubits)
            final_circuit.append_circuit(sub_circ, loc)
        else:
            # adds the unfolded original partition to the optimized_subcircuit list 
            optimized_subcircuit.append(originalSubcirc.unfold_all())
            # Merge originalSubCirq (the original partition) into the finalized circuit. Loc specifies where to append sub_circ to (which qubits)
            final_circuit.append_circuit(originalSubcirc, loc)

    final_circuit.unfold_all() # unfold any circuit gates
    
    final_circuit = bqskit_to_qiskit(final_circuit)
    
    final_circuit = transpile(final_circuit, optimization_level=0, basis_gates=['x','sx','rz','cx'])
    final_circuit = qiskit_to_bqskit(final_circuit)
    final_circuit.unfold_all()

    compiler.close()
    # Start time of the stuff after compilation
    sTime = time.time()
    
    # Save circuit

    if isinstance(save_path,str) and os.path.isdir(save_path):
        final_circuit.save(f'{save_path}/{circuit_name}_{success_threshold}_{partitionerDict[partitioner]}_{passDict[pass_type]}.qasm')

    # End time of the stuff after Compilation
    eTime = time.time()
    # Return optimized circuit, the name of the circuit, the number of gates in each partition before optimization, the number of gates
    # in each partition after optimization, the number of 2-qubit gates in each partition before optimization, the extra time taken
    # to save the circuit and the number of two-qubit gates in each partition after optimization.
    return [final_circuit, 
            f'{circuit_name}_{success_threshold}_{partitionerDict[partitioner]}_{passDict[pass_type]}.qasm', 
            sum(numGatesBeforeOptimization)/len(numGatesBeforeOptimization),
            sum(numGatesAfterOptimization)/len(numGatesAfterOptimization),
            sum(numTwoQGatesBeforeOptimizatoon)/len(numTwoQGatesBeforeOptimizatoon),
            sum(numTwoQGatesAfterOptimization)/len(numTwoQGatesAfterOptimization),
            eTime-sTime]
