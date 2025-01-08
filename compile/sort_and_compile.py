from bqskit_compile import bqskitOptimize
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

    infoDict = bqskitOptimize(qc=qc, 
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
            infoDict = bqskitOptimize(qc=file, 
                           success_threshold=success_threshold,
                           partitioner=partitioner, 
                           pass_type=pass_type, 
                           save_path=circuit_save_path,
                           replace_filter=replace_filter)
            
            # Adds the infoDict to the list of circuits 
            circuits_info.append(infoDict)
    
    return circuits_info


def optimizeBQSkit(qc: str, circuit_save_path: str, json_path: str = None, success_threshold: float = 1e-8, replace_filter: str = 'less-than-multi', 
    partitioner: int = 0, pass_type: int = 0):
    """
    Optimize circuit(s) using BQSkit. Can optimize individual files as well as directories of QASM files.

    Parameters:
        qc (str): Quantum circuit to be optimized. Path to either a QASM file or folder.

        circuit_save_path (str): Path to save the optimized quantum circuit in.

        json_path (str): Path to save JSON file containing information about the circuit.

        success_threshold (float): The distance threshold that determines successful termintation. (Default: 1e-8).

        replace_filter (str): A predicate that determines if the resulting circuit, after calling loop_body on a block, 
        should replace the original operation. (Default: less-than-multi).

        partitioner (int): Partitions circuit into blocks of 3 qubits. Supports ScanPartitioner and QuickPartitioner. 0 for
        ScanPartitioner and 1 for QuickPartitioner. (Default: 0).

        pass_type (int): Optimization algorithm to use. Supports QSearch and LEAP. 0 for QSearch, 1 for LEAP. (Default: 0).
    
        
    If there is a valid directory entered to save the JSON file to, saves JSON of optimization data to json_path. 
    If no directory is entered, returns a list containing the dictionaries that contain information about the optimized circuits.
    Saves circuit(s) to circuit_save_path.
    """
    # Function to check if json is not None
    def validJSONInput():
        if isinstance(json_path, str):
            return os.path.isdir(s=json_path)  
        if isinstance(json_path, None):
            return True
        return False

    # Checks if path is a QASM file and the save directory is valid
    if os.path.isfile(path=qc) and qc.endswith('.qasm') and os.path.isdir(path=circuit_save_path):
        
        # Checks to see if JSON input is correct
        if validJSONInput():
            # Calls optimization function and stores the dictionary returned into a variable
            infoDict = optimizeBQSkitFromFile(file=qc,
                                circuit_save_path=circuit_save_path,
                                success_threshold=success_threshold, 
                                partitioner=partitioner, 
                                pass_type=pass_type,
                                replace_filter=replace_filter)
            
            # Checks if the path is a valid directory 
            if os.path.isdir(path=json_path):

                # Gets the name of the file inputted wihtout the qasm or path
                index = qc.rfind('/')
                qc_name = qc[index+1:len(qc)-5]

                # Saves file as a json 
                file_name = f'{json_path}_{qc_name}_optimized.json'
                with open(file_name, 'w') as json_file:
                    json.dump(infoDict, json_file)
            else:
                return infoDict

        elif not validJSONInput():
            raise FileNotFoundError(f'The path {json_path} does not exist.')

    # Checks if path is a directory and the save directory is valid
    elif os.path.isdir(s=qc):
        # Checks to see if JSON input is correct
        if validJSONInput():
            # Calls optimization function
            infoDict = optimizeBQSkitFromDirectory(qc=qc, 
                                        circuit_save_path=circuit_save_path,
                                        success_threshold=success_threshold, 
                                        partitioner=partitioner, 
                                        pass_type=pass_type,
                                        replace_filter=replace_filter)
            if os.path.isdir(s=json_path):

                # Gets the name of the file inputted wihtout the qasm or path
                index = qc.rfind('/')
                qc_name = qc[index+1:len(qc)-5]

                # Saves file as a json 
                file_name = f'{json_path}_{qc_name}_optimized.json'
                with open(file_name, 'w') as json_file:
                    json.dump(infoDict, json_file)
            else:
                return infoDict
        elif not validJSONInput():
            raise FileNotFoundError(f'The path {json_path} does not exist.')
    # Raise exception if path does not exist
    elif not os.path.exists(path=qc):
        raise FileNotFoundError(f'The path {qc} does not exist.')
    elif isinstance(circuit_save_path,str) and os.path.isdir(s=circuit_save_path):
        raise FileNotFoundError(f'The path {circuit_save_path} is invalid.')
    