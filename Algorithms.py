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

def _qpe(circuit, unitary, n_precision,n_ancilla):   
    """Applies the quantum phase estimation for a given unitary.

    Parameters
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit.
    unitary(np.array): Unitary.
    n_precision(int): Number of qubits used for precision.
    n_ancilla(int): Number of qubits used for generating the eigenstates, 
                    must be len(unitary)//2 = n_ancilla.

    Output
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                    qft.
    
    """
    assert len(unitary)//2 == n_ancilla, "Ancilla qubits does't match the number needed to expand the eigenstate."    
    #Ancilla (need to add a way to initialize states)
    circuit.h([n_precision + ancilla for ancilla in range(n_ancilla)]) 
    #Precision
    circuit.h(range(n_precision))
    #Build unitary
    U = qsk.extensions.UnitaryGate(unitary, label='U')
    U_ctrl = add_control(U, num_ctrl_qubits=1, label='Controlled_U',ctrl_state=1)    
    repetitions = 1
    for counting_qubit in range(n_precision):
        for _ in range(repetitions):                        
            circuit.append(U_ctrl, [counting_qubit,*[n_precision + ancilla for ancilla in range(n_ancilla)]])         
        repetitions *= 2
    inverse_QFT(circuit,n_precision)    
    return circuit

def QPE(circuit, unitary, n_precision,n_ancilla):
    """Applies the quantum phase estimation for a given unitary.

    Parameters
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit.
    unitary(np.array): Unitary.
    n_precision(int): Number of qubits used for precision.
    n_ancilla(int): Number of qubits used for generating the eigenstates, 
                    must be len(unitary)//2 = n_ancilla.

    Output
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                    qft.
    
    """
    n_qubits = n_precision + n_ancilla
    qpe_circuit= _qpe(qsk.QuantumCircuit(n_qubits, name='QPE'), unitary, n_precision, n_ancilla)
    circuit.append(qpe_circuit, circuit.qubits[:n_qubits])
    return circuit.decompose()