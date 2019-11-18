# Introduction-to-IBM_Qiskit

## Instalation

The safe way to use the Qiskit is using conda virtual environment. After installing Anaconda 3, you do the following commands:

1) conda create -n qiskit_env python=3

2) source activate qiskit_env 

Now you install Qiskit:

- pip install qiskit

- pip install qiskit-terra[visualization]

To put this environtmen on your jupyter notebook environment you need to type the following comands:

- conda install jupyter

- conda install nb_conda

- conda install ipykernel

- python -m ipykernel install --user --name qiskit_env

In order to test if the qiskit is installed you import on your python enviroment. 

## Codes

- Initial Tutorial

    In this code you will learn:
    
        - Build a simple circuit that creates a bell state using Hadamard and C-Not gates.
        
        - Simulate your circuit theoretically  to get the state vector.
        
        - Build a real circuit that measures your Qubits in order to give bits of information.
        
        - Simulate measurement circuits that can be applied to real quantum computers.
        
        - Run your circuit in the a Real Quantum Computer.
        
        
- Deutsch Algorithm

    In this code you will see the first application of a quantum computer predicting if a boolean function is balanced or constant with only one query.


- Quantum Fourier Transform

    In this code you will learn one of the building blocks of inumerous algorithms in Quantum Computing.