import json
import os
from predetermined.optimizationSetup import optimizations
from pathlib import Path
from construct_benchmarks.construct_bqskit_benchmarks import (construct_bqskit_circSU2, 
                                                              construct_bqskit_dtc_unitary, 
                                                              construct_bqskit_QV, 
                                                              construct_bqskit_random_clifford)
from construct_benchmarks.construct_qiskit_benchmarks import (construct_qiskit_clifford_circuit,
                                                              construct_qiskit_dtc_unitary,
                                                              construct_qiskit_multi_control_circuit)
import random
from qiskit import QuantumCircuit
from bqskit.ir import Circuit

def predeterminedCompilation(qc: str = None, save_path: str = None, success_threshold: float = 1e-8, replace_filter: str = 'always', 
    partitioner: int = 0, json_path: str = None, generate_circuit: bool = False, generate_circuit_num_qubits: int = 10, generated_circuit_save_path: str = None):
    
    """
    Optimizes a function using QSearch, Leap, and Qiskit transpilation with optimization level 3.

    Parameters:
        qc (str): Quantum circuit to be optimized. Path directory to QASM file. (Default: None)
        
        save_path (str): Path to save the optimizedquantum circuits to. (Default: None)
        
        success_threshold (float): The distance threshold that determines successful termintation. (Default: 1e-8)
        
        replace_filter (str): A predicate that determines if the resulting circuit, after calling loop_body on a block, 
        should replace the original operation. (Default: 'always'). Supports 'less-than', 'always', and 'less-than-multi'.

        partitioner (int): Partitions circuit into blocks of 3 qubits. Supports ScanPartitioner and QuickPartitioner. 0 for
        ScanPartitioner and 1 for QuickPartitioner. (Default: 0).

        json_path (str): Path to save JSON file containing informdation about the circuit.
        
        generate_circuit (bool): Option to compile a random algorithmic circuit instead of inputting a circuit to compile. 
        If this is set to true, do not enter a qc parameter. (Default: False)
        
        generate_circuit_num_qubits (int): Number of qubits in the randomly generated algorithmic circuit. (Default: 10) 
        
        generated_circuit_save_path (str): Path to save the randomly generated circuit to. (Default: None)

    Returns:
        If one circuit is compiled, returns a list of dictionaries containing information about the optimization process. If multiple
        circuits are compiled, returns a list of lists of dictionaries containing information about the optimiztaion process.
    """
    # Runs if generate_circuit is true and there is no value in qc.
    # Ranomly generates a quantum circuit instead of taking an input from qc.
    if generate_circuit and qc == None:
        
        # Raises an exception if qc is not null
        if not qc == None:
            raise Exception('If generate circuit is True, qc cannot contain a path string.')
        
        # List of all the different circuit constructor functiosn
        random_circuits = [lambda: construct_bqskit_circSU2(num_qubits=generate_circuit_num_qubits, num_reps=3, save_path=generated_circuit_save_path),
                           lambda: construct_bqskit_dtc_unitary(num_qubits=generate_circuit_num_qubits, save_path=generated_circuit_save_path),
                           lambda: construct_bqskit_QV(num_qubits=generate_circuit_num_qubits, depth=None, save_path=generated_circuit_save_path),
                           lambda: construct_bqskit_random_clifford(num_qubits=generate_circuit_num_qubits, save_path=generated_circuit_save_path),
                           lambda: construct_qiskit_clifford_circuit(num_qubits=generate_circuit_num_qubits, save_path=generated_circuit_save_path),
                           lambda: construct_qiskit_dtc_unitary(num_qubits=generate_circuit_num_qubits, save_path=generated_circuit_save_path),
                           lambda: construct_qiskit_multi_control_circuit(num_qubits=generate_circuit_num_qubits, save_path=generated_circuit_save_path)]
        
        # Gets a random index in random_circuits
        random_circuit = random.randint(0, len(random_circuits) - 1)
        
        # Calls the functiion at that index and stores the list that it returns
        circuit = random_circuits[-1]()
        
        # Starts the optimization process using the inputted parameters
        circuitData = optimizations(qc=circuit[0],
                                    save_path=save_path,
                                    success_threshold=success_threshold,
                                    replace_filter=replace_filter,
                                    partitioner=partitioner,
                                    generate_circuit=generate_circuit,
                                    circuit_name=circuit[1])
        
        # Saves data as a json if a valid json save path is entered
        if isinstance(json_path, str) and os.path.isdir(json_path):
            qc_name = circuit[1][:len(circuit[1])-5]
            file_name = f'{json_path}/{qc_name}_optimized.json'
            with open(file_name, 'w') as json_file:
                json.dump(circuitData, json_file)
        # If there is no json path to save to, returns data as a list of dictionaries
        else:
            return circuitData
        
    # Runs if qc is a file and generate_circuit is false
    elif qc.endswith('.qasm') and not generate_circuit:
        # Starts the optimization process with the inputted parameters
        circuitData = optimizations(qc=qc,
                                    save_path=save_path,
                                    success_threshold=success_threshold,
                                    replace_filter=replace_filter,
                                    partitioner=partitioner
                                    )
        
        # Saves data as a json if a valid json save path is entered
        if isinstance(json_path, str) and os.path.isdir(json_path):
            index = qc.rfind('/')
            qc_name = qc[index+1:len(qc)-5]
            file_name = f'{json_path}/{qc_name}_optimized.json'
            with open(file_name, 'w') as json_file:
                json.dump(circuitData, json_file)
        # If there is no json path to save to, returns data as a list of dictionaries
        else:
            return circuitData
        
    # Runs if qc is a directory and generate_circuit is false
    elif os.path.isdir(qc) and not generate_circuit:

        # Gets all the paths to the files in the directory and stores them in a list
        folder = Path(qc)
        files = [str(file) for file in folder.iterdir() if file.is_file()]
        
        # List to store the data returned by the circuits
        circuitsData = []
        # Iterates over the files
        for file in files:
            # Starts optimization process if the file is a QASM file
            if file.endswith('qasm'):
                circuitData = optimizations(qc=file,
                                             save_path=save_path,
                                             success_threshold=success_threshold,
                                             replace_filter=replace_filter,
                                             partitioner=partitioner)
                # Adds the data of an optimized circuit to the list that stores the data
            circuitsData.append(circuitData)
        # If there is a valid path to save a JSON to, saves data as a JSON
        if isinstance(json_path,str) and os.path.isdir(json_path):
            index = qc.rfind('/')
            qc_name = qc[index+1:]
            
            flat_list = [item for sublist in circuitsData for item in sublist]
            # Saves file as a json 
            file_name = f'{json_path}/{qc_name}_optimized.json'
            with open(file_name, 'w') as json_file:
                json.dump(flat_list, json_file)
        # If the data is not saved as a JSON, returns data as a list of lists of dictionaries
        else:
            return circuitsData
