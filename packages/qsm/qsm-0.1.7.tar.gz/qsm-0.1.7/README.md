## Example of my module
                                                                                  
    import qsm 

    qc = qsm.QuantumCircuit(2)
    qc.apply_gate(qsm.H, 1) # apply the hadamar gate
    qc.apply_controlled_gate(qsm.CX, 0, 1) # 0 is the target qubit and 1 is the controll qubit 
    print(qc.get_state())
    print(qc.prob())
    print(qc.measure())