import json
import os
from predetermined.optimizationSetup import optimizations
from pathlib import Path

def predeterminedCompilation(qc: str, save_path: str = None, success_threshold: float = 1e-8, replace_filter: str = 'less-than-multi', 
    partitioner: int = 0, json_path: str = None):
    
    """
    Optimizes a function using QSearch, Leap, and Qiskit transpilation with optimization level 3.

    Parameters:
        qc (str): Quantum circuit to be optimized. Path directory to QASM file.
        
        save_path (str): Path to save quantum circuits to. (Default: None)
        
        success_threshold (float): The distance threshold that determines successful termintation. (Default: 1e-8)
        
        replace_filter (str): A predicate that determines if the resulting circuit, after calling loop_body on a block, 
        should replace the original operation. (Default: 'always'). Supports 'less-than', 'always', and 'less-than-multi'.

        partitioner (int): Partitions circuit into blocks of 3 qubits. Supports ScanPartitioner and QuickPartitioner. 0 for
        ScanPartitioner and 1 for QuickPartitioner. (Default: 0).

        json_path (str): Path to save JSON file containing informdation about the circuit.

    Returns:
        If one circuit is compiled, returns a list of dictionaries containing information about the optimization process. If multiple
        circuits are compiled, returns a list of lists of dictionaries containing information about the optimiztaion process.
    """

    if qc.endswith('.qasm'):
        circuitData = optimizations(qc=qc,
                                    save_path=save_path,
                                    success_threshold=success_threshold,
                                    replace_filter=replace_filter,
                                    partitioner=partitioner
                                    )
        if isinstance(json_path, str) and os.path.isdir(json_path):
            index = qc.rfind('/')
            qc_name = qc[index+1:len(qc)-5]
            file_name = f'{json_path}/{qc_name}_optimized.json'
            with open(file_name, 'w') as json_file:
                json.dump(circuitData, json_file)
        else:
            return circuitData
    elif os.path.isdir(qc):

        folder = Path(qc)
        files = [str(file) for file in folder.iterdir() if file.is_file()]
        circuitsData = []
        for file in files:
            if file.endswith('qasm'):
                 circuitData = optimizations(qc=file,
                                             save_path=save_path,
                                             success_threshold=success_threshold,
                                             replace_filter=replace_filter,
                                             partitioner=partitioner)
                 circuitsData.append(circuitData)
        if isinstance(json_path,str) and os.path.isdir(json_path):
            index = qc.rfind('/')
            qc_name = qc[index+1:]

            # Saves file as a json 
            file_name = f'{json_path}/{qc_name}_optimized.json'
            with open(file_name, 'w') as json_file:
                json.dump(circuitsData, json_file)
        else:
            return circuitsData
    else:
        if not save_path == None:
            raise Exception('Some parameter is wrong.')