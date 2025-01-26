from predetermined.compile import predeterminedCompilation
from bqskit.ir import Circuit

if __name__ == '__main__':
   """
   predeterminedCompilation(qc='benchmark_circuits/clifford_10_98001.qasm',
                            save_path='compiled_circuits',
                            json_path='compiled_circuits',
                            replace_filter='less-than-multi'
                            )
   
   qc = Circuit.from_file('benchmark_circuits/clifford_10_98001.qasm')
   print(qc.gate_counts)
   """
   
   qc = '432432/fadsf/4324agga.qasm'
   index = qc.rfind('/')
   qc_name = qc[index+1:len(qc)-5]
   print(qc_name)

    
    

    
