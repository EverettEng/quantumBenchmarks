from compile.sort_and_compile import optimizeBQSkit
from bqskit.ir import Circuit 

if __name__ == '__main__':
    """
    Test code below 
    
    qc = 'benchmark_circuit_folders/bqskit/su2'
    circuit_save_path = 'benchmark_circuit_folders/optimized_bqskit/su2'
    json_path = 'benchmark_circuit_folders/optimized_bqskit/su2_json'
    optimizeBQSkit(qc=qc,
                    circuit_save_path=circuit_save_path,
                    json_path=json_path,
                    success_threshold=1e-8,
                    partitioner=1,
                    pass_type=1
                   )
    """
    print('Compilation task finished')