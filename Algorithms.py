import qiskit as qsk 
import numpy as np
from qiskit.circuit.add_control import add_control

def _qft(circuit, qregister):
    """ QFT on a circuit.

    Parameters
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit.
    qregister(qiskit.QuantumRegister): Quantum register for the rotation.

    Output
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                    qft.
    
    """    
    
    def qft_rotations(circuit, qregister):
        """ Defines the rotations necessary for the QFT
        in a recursive manner.

        Parameters
        ------------------------------------------------
        circuit(qiskit.QuantumCircuit): Quantum Circuit.
        qregister(qiskit.QuantumRegister): Quantum register for the rotation.

        Output
        ------------------------------------------------
        circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                        qft.

        """
        for i in reversed(qregister):
            circuit.h(i)
            for qubit in range(i.index):
                circuit.cu1(np.pi/float(2**(i.index-qubit)), qregister[qubit], qregister[i.index])    
        return circuit    

    def qft_swap(circuit, qregister):
        """Swap registers for the QFT.
        
        Parameters
        ------------------------------------------------
        circuit(qiskit.QuantumCircuit): Quantum Circuit.
        n(int): qubit to do the rotation.

        Output
        ------------------------------------------------
        circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                        qft.
        """
        n = len(qregister)
        for qubit in range(n//2):
            circuit.swap(qregister[qubit], qregister[n-qubit-1])
        return circuit

    qft_rotations(circuit,qregister)
    qft_swap(circuit, qregister)
    return circuit

def qft(circuit,qregister):
    """QFT. 

    Parameters
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit.
    qregister(qiskit.QuantumRegister): Quantum register for the rotation.

    Output
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                    qft.
    
    """
    qft_circuit= _qft(qsk.QuantumCircuit(qregister, name='QFT'), qregister)
    circuit.append(qft_circuit, qregister)
    return circuit

def inverse_QFT(circuit,qregister):
    """ Inverse QFT. 

    Parameters
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit.
    qregister(qiskit.QuantumRegister): Quantum register for the rotation.

    Output
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                    qft.
    
    """
    qft_circuit= _qft(qsk.QuantumCircuit(qregister, name='QFT'), qregister)
    inverseqft = qft_circuit.inverse()
    circuit.append(inverseqft, qregister)
    return circuit

def qpe(circuit, unitary, precision, ancilla, init_state=None):   
    """Applies the quantum phase estimation for a given unitary.

    Parameters
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit.
    unitary(np.array): Unitary.
    precision(QuantumRegister): Quantum register for the precision of the QPE.
    ancilla(QuantumRegister): Quantum register for the ancilla,
                   must be len(unitary)//2 = n_ancilla.
    init_state(list): Initial state for the ancilla qubit.

    Output
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                    qft.
    
    """
    #n_precision = len(precision)
    n_ancilla = len(ancilla)
    assert len(unitary)//2 == n_ancilla, "Ancilla qubits does't match the number needed to expand the eigenstate."    
    
    #Ancilla (need to add a way to initialize states)    
    if init_state is not None:
        assert len(init_state) == 2**n_ancilla , "Initial state not valid."
        circuit.initialize(init_state, ancilla)
            
    #Precision
    circuit.h(precision)
    #Build unitary
    U = qsk.extensions.UnitaryGate(unitary, label='U')
    U_ctrl = add_control(U, num_ctrl_qubits=1, label='Controlled_U',ctrl_state=1)    
    repetitions = 1
    for counting_qubit in precision:
        for _ in range(repetitions):                        
            circuit.append(U_ctrl, [counting_qubit,ancilla])         
        repetitions *= 2
    inverse_QFT(circuit, precision)   
    
    return circuit

def QPE(circuit, unitary, precision, ancilla, init_state=None):
    """ Inverse QPE. 

    Parameters
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit.
    unitary(np.array): Unitary.
    precision(QuantumRegister): Quantum register for the precision of the QPE.
    ancilla(QuantumRegister): Quantum register for the ancilla,
                   must be len(unitary)//2 = n_ancilla.
    init_state(list): Initial state for the ancilla qubit.

    Output
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                    qft.
    
    """
    qpe_circuit = qsk.QuantumCircuit(precision, name='QPE')
    qpe_circuit.add_register(ancilla)
    qpe_circuit= qpe(qpe_circuit, unitary, precision, ancilla, init_state=init_state)    
    
    append_qbits = [i for i in precision]
    for i in ancilla:
        append_qbits.append(i)
    
    circuit.append(qpe_circuit, append_qbits)
    return circuit

def inverse_QPE(circuit, unitary, precision, ancilla, init_state=None):
    """ Inverse QPE. 

    Parameters
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit.
    unitary(np.array): Unitary.
    precision(QuantumRegister): Quantum register for the precision of the QPE.
    ancilla(QuantumRegister): Quantum register for the ancilla,
                   must be len(unitary)//2 = n_ancilla.
    init_state(list): Initial state for the ancilla qubit.

    Output
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                    qft.
    
    """
    qpe_circuit = qsk.QuantumCircuit(precision, name='QPE')
    qpe_circuit.add_register(ancilla)
    qpe_circuit= qpe(qpe_circuit, unitary, precision, ancilla, init_state=init_state)    
    inverseqpe = qpe_circuit.inverse()
    append_qbits = [i for i in precision]
    for i in ancilla:
        append_qbits.append(i)
    circuit.append(inverseqpe, append_qbits)
    return circuit