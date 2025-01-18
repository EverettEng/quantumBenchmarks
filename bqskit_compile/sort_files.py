from bqskit_compile.bqskitTests import optimizationAnalysis
import os
from pathlib import Path
from bqskit.ir import Circuit
import json

def optimizeBQSkitFromFile(qc: str, circuit_save_path: str, success_threshold: float = 1e-8, replace_filter: str = 'less-than-multi', 
    partitioner: int = 0, pass_type: int = 0):
    """
    Optimize a circuit using BQSkit from a QASM file 

    Parameters:

        qc (str): Quantum circuit to be optimized. Path directory to QASM file.

        circuit_save_path (str): Path to save the optimized quantum circuit in.

        json_path (str): Path to save JSON file containing information about the circuit.

        success_threshold (float): The distance threshold that determines successful termintation. (Default: 1e-8).

        replace_filter (str): A predicate that determines if the resulting circuit, after calling loop_body on a block, 
        should replace the original operation. (Default: less-than-multi).

        partitioner (int): Partitions circuit into blocks of 3 qubits. Supports ScanPartitioner and QuickPartitioner. 0 for
        ScanPartitioner and 1 for QuickPartitioner. (Default: 0).

        pass_type (int): Optimization algorithm to use. Supports QSearch and LEAP. 0 for QSearch, 1 for LEAP. (Default: 0).

    Returns:
    
        Dictionary contianing information about the circuit before/after optimization inside a list.
    """

    infoDict = optimizationAnalysis(qc=qc, 
                   save_path=circuit_save_path, 
                   success_threshold=success_threshold, 
                   partitioner=partitioner, 
                   pass_type=pass_type,
                   replace_filter=replace_filter)
    
    circuit_list = [infoDict]

    return circuit_list

def optimizeBQSkitFromDirectory(qc: str, circuit_save_path: str, success_threshold: float = 1e-8, replace_filter: str = 'less-than-multi', 
    partitioner: int = 0, pass_type: int = 0):
    """
    Optimize a circuit using BQSkit from a QASM file.

    Parameters:

        qc (str): Quantum circuit to be optimized. Path directory to QASM file.

        circuit_save_path (str): Path to save the optimized quantum circuit in.

        json_path (str): Path to save JSON file containing information about the circuit.

        success_threshold (float): The distance threshold that determines successful termintation. (Default: 1e-8).

        replace_filter (str): A predicate that determines if the resulting circuit, after calling loop_body on a block, 
        should replace the original operation. (Default: less-than-multi).

        partitioner (int): Partitions circuit into blocks of 3 qubits. Supports ScanPartitioner and QuickPartitioner. 0 for
        ScanPartitioner and 1 for QuickPartitioner. (Default: 0).

        pass_type (int): Optimization algorithm to use. Supports QSearch and LEAP. 0 for QSearch, 1 for LEAP. (Default: 0).

    Returns:

        List of dictionaries that each contain information about circuit before/after optimization.
    """

    # Creates list of paths to files. 
    folder = Path(qc)
    files = [str(file) for file in folder.iterdir() if file.is_file()]

    # List of dictionaries that each cotain information about a circuits before/after optimization
    circuits_info = []

    # Optimizes each file if it is a QASM file
    for file in files:
        if file.endswith('.qasm'):
            # Assigns the dictionary to infoDict
            infoDict = optimizationAnalysis(qc=file, 
                           success_threshold=success_threshold,
                           partitioner=partitioner, 
                           pass_type=pass_type, 
                           save_path=circuit_save_path,
                           replace_filter=replace_filter)
            
            # Adds the infoDict to the list of circuits 
            circuits_info.append(infoDict)
    
    return circuits_info


