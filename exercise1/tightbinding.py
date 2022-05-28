'''
IBM Quantum Spring Challenge 2022
Exercise 1: Tight-binding model
'''

import numpy as np
import matplotlib.pyplot as plt

import qiskit
from qiskit import QuantumCircuit, QuantumRegister
import qiskit.quantum_info as qi


#### 2.1 building the individual Pauli unitaries

def U_step(nq: int):
    '''
    Build the circuit corresponding to the single trotter step unitary operator
    U(dt) = \sum_i ( e^{-i dt X_i ^ X_i+1} e^{-i dt Y_i ^ Y_i+1} )
    '''
    assert(isinstance(nq, int));

    # define time as parameter of qubit operations
    from qiskit.circuit import Parameter
    t = Parameter('t')
    
    # example code: ZZ subcircuit where ZZ := exp(-it Z_i ^ Z_j)
    ZZ_qr = QuantumRegister(2)
    ZZ_qc = QuantumCircuit(ZZ_qr, name='ZZ')
    ZZ_qc.cnot(0,1)
    ZZ_qc.rz(2 * t, 1)
    ZZ_qc.cnot(0,1)
    ZZ = ZZ_qc.to_instruction() # Convert circuit into a gate (Instruction object)
    # end example code (not mine)

    # Q 1a: build XX(2t) out of ZZ(2t)
    XX_qr = QuantumRegister(2)
    XX_qc = QuantumCircuit(XX_qr, name='XX')

    # hadamard to rotate X into Z
    for qubiti in range(len(XX_qc.qubits)):
        XX_qc.h(qubiti);

    # perform ZZ
    XX_qc.append(ZZ, [0,1])

    # hadamard to rotate Z back into X
    for qubiti in range(len(XX_qc.qubits)):
        XX_qc.h(qubiti);

    # Convert custom quantum circuit into a gate
    XX = XX_qc.to_instruction();

    my = QuantumCircuit(QuantumRegister(2))
    my.append(XX, [0,1])
    my = my.bind_parameters({t: 1.0})
    print(qi.Operator(my)); assert False;

    # Q 1b: build YY(2t) out of ZZ(2t)
    YY_qr = QuantumRegister(2)
    YY_qc = QuantumCircuit(YY_qr, name='YY')

    for qubiti in range(len(YY_qc.qubits)):
        YY_qc.sdg(qubiti); # S^dag gate to rotate Y into -X
        YY_qc.u(2*np.pi,0,0,qubiti); # (-1) to take -X to X
        YY_qc.h(qubiti); # hadamard to rotate X into Z

    YY_qc.append(ZZ, [0,1])

    for qubiti in range(len(YY_qc.qubits)):
        YY_qc.h(qubiti); # Z back into X
        YY_qc.s(qubiti); # X back into Y
        
    # Convert custom quantum circuit into a gate
    YY = YY_qc.to_instruction();

    # example code: put all together as single trotter step circuit
    Trot_qr = QuantumRegister(nq)
    Trot_qc = QuantumCircuit(Trot_qr, name='Trot')

    for i in range(0, nq - 1):
        Trot_qc.append(YY, [Trot_qr[i], Trot_qr[i+1]]);
        Trot_qc.append(XX, [Trot_qr[i], Trot_qr[i+1]]);

    print(Trot_qc.draw());

    return Trot_qc.to_instruction();


def U_trotter(t_target, trotter_steps) -> QuantumCircuit:
    '''
    '''

    qr = QuantumRegister(3)
    qc = QuantumCircuit(qr)
    Trot_gate = U_step(3);

    for i in range(trotter_steps):
        qc.append(Trot_gate, list(range(3)));

    print(qc.draw())


#################################################################
#### run code
if(__name__ == '__main__'):
    U_trotter(1.0,3);
