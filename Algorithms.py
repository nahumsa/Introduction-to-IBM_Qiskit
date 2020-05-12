import qiskit as qsk 
import numpy as np

def _qft(circuit, n):
    """ QFT on a circuit.

    Parameters
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit.
    n(int): qubit to do the rotation.

    Output
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                    qft.
    
    """    
    
    def qft_rotations(circuit, n):
        """ Defines the rotations necessary for the QFT
        in a recursive manner.

        Parameters
        ------------------------------------------------
        circuit(qiskit.QuantumCircuit): Quantum Circuit.
        n(int): qubit to do the rotation.

        Output
        ------------------------------------------------
        circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                        qft.

        """
        for i in reversed(range(n)):
            circuit.h(i)
            for qubit in range(i):
                circuit.cu1(np.pi/float(2**(i-qubit)), qubit, i)    
        return circuit    

    def qft_swap(circuit, n):
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
        for qubit in range(n//2):
            circuit.swap(qubit, n-qubit-1)
        return circuit

    qft_rotations(circuit,n)
    qft_swap(circuit, n)
    return circuit

def qft(circuit,n):
    """QFT. 

    Parameters
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit.
    n(int): qubit to do the rotation.

    Output
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                    qft.
    
    """
    qft_circuit= _qft(qsk.QuantumCircuit(n, name='QFT'), n)
    circuit.append(qft_circuit, circuit.qubits[:n])
    return circuit.decompose()

def inverse_QFT(circuit,n):
    """ Inverse QFT. 

    Parameters
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit.
    n(int): qubit to do the rotation.

    Output
    ------------------------------------------------
    circuit(qiskit.QuantumCircuit): Quantum Circuit with
                                    qft.
    
    """
    qft_circuit= _qft(qsk.QuantumCircuit(n, name='QFT'), n)
    inverseqft = qft_circuit.inverse()
    circuit.append(inverseqft, circuit.qubits[:n])
    return circuit.decompose()