'''
IBM Quantum Spring Challenge 2022
Exercise 1: Tight-binding model
'''

import numpy as np
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
