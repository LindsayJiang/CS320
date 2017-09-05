#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3
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


#2.a.
def increment(addr):
    return \
           copy(addr, 1) + \
            ['set 2 1', 'add'] + \
            copy(0, addr)


#2.b.
def decrement(addr):
    return \
            copy(addr, 1) + \
           ['set 2 -1', 'add'] + \
           copy(0, addr)


#2.c.
def call(name):
    return \
            decrement(7) + \
            ['set 3 7', \
             'set 4 4', \
             'copy', \
             'set 3 6', \
             'copy'] + \
            ['set 3 7', \
             'set 4 3', \
             'copy', \
             'set 4 1', \
             'copy'] + \
            ['set 2 14', \
             'add', \
             'set 3 7', \
             'set 4 4', \
             'copy', \
             'set 3 0', \
             'copy'] + \
            ['goto ' + name + '_start'] + \
            increment(7)
        

#2.d.
def procedure(name, body):
    return \
           ['goto' + ' ' + name + '_end'] + \
           ['label' +  ' ' + name + '_start'] + \
           body + \
           ['set 3 7', \
            'set 4 3', \
            'copy', \
            'set 4 0', \
            'copy'] + \
           ['jump 0'] + \
           ['label' + ' ' + name + '_end']
# eof
