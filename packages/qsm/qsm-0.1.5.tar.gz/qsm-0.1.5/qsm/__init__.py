import numpy as np

from qsm.qubit import *
from qsm.gate_library import *
from qsm.instruction import *
from qsm.utils import *

pi = np.pi

class QuantumCircuit:
    def __init__(self, num_qubits):
        self.qubits = Qubit(num_qubits)

    def h(self, qubit):
        self.customgate(qubit, hadamard())

    def cx(self, qubit_control, qubit_target):
        self.custom_control(qubit_control, qubit_target, cnot_controller, paulix())
    def custom_control(self, qubit_control, qubit_target, controller, matrix):
        gate = Controlled2By2Gate(Instruction(matrix), controller)
        self.qubits.apply_controlled_gate(gate, qubit_control, qubit_target)

    def x(self, qubit):
        self.customgate(qubit, paulix())

    def y(self, qubit):
        self.customgate(qubit, pauliy())
    def z(self, qubit):
        self.customgate(qubit, pauliz())

    def s(self, qubit):
        self.customgate(qubit, s())

    def sdg(self, qubit):
        self.customgate(qubit, sdg())

    def t(self, qubit):
        self.customgate(qubit, t())

    def tdg(self, qubit):
        self.customgate(qubit, tdg())

    def u3(self, theta, phi, lamba, qubit):
        self.customgate(qubit, u(theta, phi, lamba))

    def u2(self, phi, lamba, qubit):
        self.customgate(qubit, u(pi/2, phi, lamba))

    def u1(self, lamba, qubit):
        self.customgate(qubit, u(0, 0, lamba))

    def toffolie(self, qubit_control1, qubit_control2, qubit_target):
        self.h(qubit_target)
        self.cx(qubit_control2, qubit_target)
        self.tdg(qubit_target)
        self.cx(qubit_control1, qubit_target)
        self.t(qubit_target)
        self.cx(qubit_control2, qubit_target)
        self.tdg(qubit_target)
        self.t(qubit_control2)
        self.cx(qubit_control1, qubit_target)
        self.t(qubit_target)
        self.cx(qubit_control1, qubit_control2)
        self.h(qubit_target)
        self.tdg(qubit_control2)
        self.t(qubit_control1)
        self.cx(qubit_control1, qubit_control2)

    def swap(self, qubit1, qubit2):
        gate_inst = Instruction(swap())
        gate = ControlledGate(gate_inst)
        self.qubits.apply_controlled_gate(gate, qubit1, qubit2)

    def cz(self, qubit_control, qubit_target):
        gate_inst = Instruction(pauliz())
        gate = Controlled2By2Gate(gate_inst, None)
        self.qubits.apply_controlled_gate(gate, qubit_target, qubit_control)

    def customgate(self, qubit, matrix):
        gate_inst = Instruction(matrix)
        gate = SingelletonGate(gate_inst)
        self.qubits.apply_gate(gate, qubit)

    def state_vector(self):
        return np.round(self.qubits.state, decimals=3)

    def probabilities(self):
        self.qubits.state /= np.linalg.norm(self.qubits.state)
        return np.abs(self.qubits.state) ** 2

    def measure_all(self, shots=1000):
        prob = self.probabilities()
        stringrep = possible_bits(self.qubits.state)
        args = initial_dict_state(self.qubits.state)
        for i in range(shots):
            measure = np.random.choice(stringrep, p=prob)
            args[measure] += 1

        return args

    def measure(self, qubits_to_measure, shots=1000):
        prob = self.probabilities()
        stringstate = possible_bits(self.qubits.state)
        args = initial_dict_list(qubits_to_measure)
        for i in range(shots):
            measure = np.random.choice(stringstate, p=prob)
            measured_result = measure[min(qubits_to_measure):max(qubits_to_measure)+1]
            args[measured_result] += 1
            # Mise à jour de l'état quantique après mesure
            measured_result_indices = [int(bit) for bit in measured_result[::-1]]

            # Mise à zéro des qubits mesurés dans l'état
            for qubit in qubits_to_measure:
                measured_result_indices[qubit] = 0

            measured_result_index = sum(measured_result_indices)
            self.qubits.state[measured_result_index] = 0

        self.qubits.state /= np.linalg.norm(self.qubits.state)

        return args
