from bqskit.compiler import Compiler
from bqskit.ir import Circuit
from bqskit.passes import QSearchSynthesisPass, QuickPartitioner, UnfoldPass, LEAPSynthesisPass, ScanPartitioner
import os

blockSize = 3
partitionerDict = {
        0: f'ScanPartitioner{blockSize}',
        1: f'QuckPartitioner{blockSize}'
    }
passDict = {
    0: 'QSearch',
    1: 'LEAP'
}

def analyzePartitions(qc: str, pass_type: int, partitioner: int, success_threshold: float, save_path: str, replace_filter: str):
# CURRENTLY REPLACE FILTER TAKES VERY LONG
    """
    Simulates a ForEachBlockPass

    Parameters:
        qc (str): Quantum circuit to be optimized. Path directory to QASM file.

        pass_type (int): Optimization algorithm to use. Supports QSearch and LEAP. 0 for QSearch, 1 for LEAP. (Default: 0).

        partitioner (int): Partitions circuit into blocks of 3 qubits. Supports ScanPartitioner and QuickPartitioner. 0 for
        ScanPartitioner and 1 for QuickPartitioner. (Default: 0).

        success_threshold (float): The distance threshold that determines successful termintation. (Default: 1e-8).

        save_path (str): The fie path to save the string to

        replace_filter (str): A predicate that determines if the resulting circuit, after calling loop_body on a block, 
        should replace the original operation. (Default: less-than-multi). Support for less-than and less-than-multi.


    Returns:
        Optimized circuit saved to the save_path and a dictionary containing information about the optimization process.
    """

    replace_filter_condition_met = False

    while not replace_filter_condition_met:
        passes = [QSearchSynthesisPass(success_threshold=success_threshold), 
                LEAPSynthesisPass(success_threshold=success_threshold)]
   
        partitioners = [ScanPartitioner(block_size=blockSize), 
                        QuickPartitioner(block_size=blockSize)]
    
        # Instantiate compiler and get the file
        compiler = Compiler()
        circuit = Circuit.from_file(filename=qc)

        # Unfolds all gates
        circuit.unfold_all()

        # Compiles using quickpartitioner
        out = compiler.compile(circuit, partitioners[partitioner])

        # Workflow
        optimization_workflow = [passes[pass_type], UnfoldPass()]

        # Ids of submitted sub-circuits
        ids = []

        # Respective locations in the original circuit
        locations = []

        # Iterates over each partition of the compiled circuit (out)
        for partition in out:
            # Appends the location of the partition in the original circuit to the locations list
            locations.append(partition.location)

            # Creates a sub_circuit from the partition
            sub_circ = Circuit.from_operation(partition)

            # Unfolds gates in sub_circ
            sub_circ.unfold_all()

            # Submits a compilation task using the workflow above to the compiler. Returns an ID that represents the completed task
            id = compiler.submit(sub_circ, optimization_workflow)

            # appends the ID of the compilation task to the ID list, allowing for the tracking of the partition optimizations 
            ids.append(id)


        # Checks the status of all submitted circuits, waiting until they are all compiled (status 2)
        while all(compiler.status(id) != 2 for id in ids):
            continue

        # New circuit is instantiated to hold the final optimized circuits, initialized with the same amount of qudits as the original circuit
        final_circuit = Circuit(num_qudits=circuit.num_qudits)

        # List of the optimized subcircuits
        optimized_subcircuit = []

        for id, loc in zip(ids, locations):

            # retrieves the result by calling the compiled partition's ID
            sub_circ = compiler.result(id)

            # adds the unfolded optimized partition to the optimized_subcircuit list 
            optimized_subcircuit.append(sub_circ.unfold_all())

            # Merge sub_circ (the optimized partition) into the finalized circuit. Loc specifies where to append sub_circ to (which qubits)
            final_circuit.append_circuit(sub_circ, loc)

        final_circuit.unfold_all() # unfold any circuit gates

        compiler.close()

        # get the name of the QASM file without the .qasm
        index = qc.rfind('/')
        file_name = qc[index+1:len(qc)-5]

        if replace_filter == 'less-than':
            original_num_gates = 0
            final_circuit_num_gates = 0
            for gate in circuit.gate_counts:
                original_num_gates += int(circuit.count(gate))
            for gate in final_circuit.gate_counts:
                final_circuit_num_gates += int(final_circuit.count(gate))
            if (final_circuit_num_gates < original_num_gates):
                replace_filter_condition_met = True
        

        if replace_filter == 'less-than-multi':
            compiled_two_q_gates = 0
            original_two_q_gates = 0
            for gate in circuit.gate_counts:
                if gate.num_qudits == 1:
                    continue
                original_two_q_gates += int(circuit.count(gate))
            for gate in final_circuit.gate_counts:
                if final_circuit.num_qudits == 1:
                    continue
                compiled_two_q_gates += int(final_circuit.count(gate))
            if (original_two_q_gates > compiled_two_q_gates):
                replace_filter_condition_met = True
        
        replace_filter_condition_met = True


    # Save circuit

    if isinstance(save_path,str):
        final_circuit.save(f'{save_path}/{file_name}_{success_threshold}_{partitionerDict[partitioner]}_{passDict[pass_type]}.qasm')

    # Return optimized circuit
    return [final_circuit, f'{file_name}_{success_threshold}_{partitionerDict[partitioner]}_{passDict[pass_type]}.qasm']

def presetPartitions(qc: str, pass_type: int, partitioner: int, success_threshold: float, save_path: str, replace_filter: str):
    
    replace_filter_condition_met = False

    while not replace_filter_condition_met:
        passes = [QSearchSynthesisPass(success_threshold=success_threshold, instantiate_options={'multistart': 2 ** 3}), 
                LEAPSynthesisPass(success_threshold=success_threshold, instantiate_options={'multistart': 2 ** 3})]
   
        partitioners = [ScanPartitioner(block_size=blockSize), 
                        QuickPartitioner(block_size=blockSize)]
    
        # Instantiate compiler and get the file
        compiler = Compiler()
        circuit = Circuit.from_file(filename=qc)

        # Unfolds all gates
        circuit.unfold_all()

        # Compiles using quickpartitioner
        out = compiler.compile(circuit, partitioners[partitioner])

        # Workflow
        optimization_workflow = [passes[pass_type], UnfoldPass()]

        # Ids of submitted sub-circuits
        ids = []

        # Respective locations in the original circuit
        locations = []

        # Iterates over each partition of the compiled circuit (out)
        for partition in out:
            # Appends the location of the partition in the original circuit to the locations list
            locations.append(partition.location)

            # Creates a sub_circuit from the partition
            sub_circ = Circuit.from_operation(partition)

            # Unfolds gates in sub_circ
            sub_circ.unfold_all()

            # Submits a compilation task using the workflow above to the compiler. Returns an ID that represents the completed task
            id = compiler.submit(sub_circ, optimization_workflow)

            # appends the ID of the compilation task to the ID list, allowing for the tracking of the partition optimizations 
            ids.append(id)


        # Checks the status of all submitted circuits, waiting until they are all compiled (status 2)
        while all(compiler.status(id) != 2 for id in ids):
            continue

        # New circuit is instantiated to hold the final optimized circuits, initialized with the same amount of qudits as the original circuit
        final_circuit = Circuit(num_qudits=circuit.num_qudits)

        # List of the optimized subcircuits
        optimized_subcircuit = []

        for id, loc in zip(ids, locations):

            # retrieves the result by calling the compiled partition's ID
            sub_circ = compiler.result(id)

            # adds the unfolded optimized partition to the optimized_subcircuit list 
            optimized_subcircuit.append(sub_circ.unfold_all())

            # Merge sub_circ (the optimized partition) into the finalized circuit. Loc specifies where to append sub_circ to (which qubits)
            final_circuit.append_circuit(sub_circ, loc)

        final_circuit.unfold_all() # unfold any circuit gates

        compiler.close()

        # get the name of the QASM file without the .qasm
        index = qc.rfind('/')
        file_name = qc[index+1:len(qc)-5]

        if replace_filter == 'less-than':
            original_num_gates = 0
            final_circuit_num_gates = 0
            for gate in circuit.gate_counts:
                original_num_gates += int(circuit.count(gate))
            for gate in final_circuit.gate_counts:
                final_circuit_num_gates += int(final_circuit.count(gate))
            if (final_circuit_num_gates < original_num_gates):
                replace_filter_condition_met = True
        

        if replace_filter == 'less-than-multi':
            compiled_two_q_gates = 0
            original_two_q_gates = 0
            for gate in circuit.gate_counts:
                if gate.num_qudits == 1:
                    continue
                original_two_q_gates += int(circuit.count(gate))
            for gate in final_circuit.gate_counts:
                if final_circuit.num_qudits == 1:
                    continue
                compiled_two_q_gates += int(final_circuit.count(gate))
            if (original_two_q_gates > compiled_two_q_gates):
                replace_filter_condition_met = True
        replace_filter_condition_met = True
                
    # Save circuit

    if isinstance(save_path,str) and os.path.isdir(save_path):
        final_circuit.save(f'{save_path}/{file_name}_{success_threshold}_{partitionerDict[partitioner]}_{passDict[pass_type]}.qasm')

    # Return optimized circuit
    return [final_circuit, f'{file_name}_{success_threshold}_{partitionerDict[partitioner]}_{passDict[pass_type]}.qasm']
      