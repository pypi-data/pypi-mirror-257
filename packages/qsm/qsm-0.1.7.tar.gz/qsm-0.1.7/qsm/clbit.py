from functools import reduce

import numpy as np

class MlBit:
    def __init__(self, num_bits):
        ket_zero = np.array([1, 0])
        self.clbits = [ket_zero]
        for i in range(num_bits-1):
            self.clbits.append(ket_zero)

    def change_qubit(self, index, state_num):
        if state_num == 1:
            self.clbits[index] = np.array([0, 1])
        else:
            self.clbits[index] = np.array([1, 0])

    def recieve(self):
        return reduce(np.kron, self.clbits)

    def recieve_index(self, index):
        return self.clbits[index]

    def recieve_all(self):
        return self.clbits