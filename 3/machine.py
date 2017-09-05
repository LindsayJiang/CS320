#####################################################################
#
# CAS CS 320, Spring 2015
# Assignment 3 (skeleton code)
# machine.py
#

def simulate(s):
    instructions = s if type(s) == list else s.split("\n")
    instructions = [l.strip().split(" ") for l in instructions]
    mem = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: -1, 6: 0}
    control = 0
    outputs = []
    while control < len(instructions):
        # Update the memory address for control.
        mem[6] = control 
        
        # Retrieve the current instruction.
        inst = instructions[control]
        # Handle the instruction.
        if inst[0] == 'label':
            pass
        if inst[0] == 'goto':
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'branch' and mem[int(inst[2])]:
            control = instructions.index(['label', inst[1]])
            continue
        if inst[0] == 'jump':
            control = mem[int(inst[1])]
            continue
        if inst[0] == 'set':
            mem[int(inst[1])] = int(inst[2])
        if inst[0] == 'copy':
            mem[mem[4]] = mem[mem[3]]
        if inst[0] == 'add':
            mem[0] = mem[1] + mem[2]

        # Push the output address's content to the output.
        if mem[5] > -1:
            outputs.append(mem[5])
            mem[5] = -1

        # Move control to the next instruction.
        control = control + 1

    print("memory: "+str(mem))
    return outputs

# Examples of useful helper functions from lecture.    
def copy(frm, to):
    return [\
        'set 3 ' + str(frm),\
        'set 4 ' + str(to),\
        'copy'\
        ]
#2.a
def increment(addr):
    # after incrementing, need to clean up every addr used.
    return [\
        "set 1 1"] + \
        copy(addr,2) +\
        ["add"] + \
        copy(0, addr) +\
        ["set 1 0", "set 2 0", "set 0 0", "set 3 0", "set 4 0"]

#2.b
def decrement(addr):
    # after decrementing, need to clean up every addr used.
    return [\
        "set 1 -1"] + \
        copy(addr, 2) +\
        ["add"] + \
        copy(0, addr) +\
        ["set 1 0", "set 2 0", "set 0 0", "set 3 0", "set 4 0"]

#2.c
def call(name):
    #update the integer stored in the memory address that
    #   contains the address of the top of the call stack
    #store the current program location at the top of the call stack;
    #increment the value at the top of the call stack so it refers to the
    #   location in the program to which control should return after the end of the procedure being invoked;
    #goto the procedure body that corresponds to the procedure name supplied;
    #increment the integer stored in the memory address that contains the
    #address of the top of the call stack
    return \
        decrement(7) + \
        copy(7,4) + \
        ["set 3 6", \
        "copy"] + \
        copy(7,3) +\
        ["set 4 1",\
        "copy", \
         "set 2 14", \
         "add"] +\
         copy(7,4) +\
        ["set 3 0", \
         "copy"] +\
        ["goto " + name + "_start"] +\
        increment(7)
        
#2.d
def procedure(name, body):
    # goto the end of precedure to not execute it before calling.
    # a label identifying the start of the procedure body;
    # the procedure body
    # instructions to jump back to the machine language program location
    #    that invoked the procedure;
    # a label identifying the end of the procedure body.
    return [\
        "goto" + " " + name + "_end"] +\
        ["label" + " " + name + "_start"] +\
        body +\
        copy(7,3) +\
        ["set 4 0", \
         "copy"] +\
        ["jump 0"] +\
        ["label" + " " + name + "_end"]


        
# eof
