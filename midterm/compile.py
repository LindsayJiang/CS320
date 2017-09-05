#####################################################################
#
# CAS CS 320, Spring 2015
# Midterm (skeleton code)
# compile.py
# Linshan Jiang(linshan@bu.edu)
#
#  ****************************************************************
#  *************** Modify this file for Problem #3. ***************
#  ****************************************************************
#

from random import randint
exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('optimize.py').read())
exec(open('machine.py').read())
exec(open('analyze.py').read())

Leaf = str
Node = dict

def freshStr():
    return str(randint(0,10000000))

def compileExpression(env, e, heap):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                n = children[0]
                heap = heap + 1
                return (['set ' + str(heap) + ' ' + str(n)], heap, heap)
            # Complete 'True', 'False', 'Array', and 'Plus' cases for Problem #3.
            if label == "Variable":
                t = children[0]
                v = env[t]
                heap = heap + 1
                insts = copy(v, heap)
                return (insts, heap, heap)
            if label == "Plus":
                e1 = children[0]
                e2 = children[1]
                heap += 1
                (insts1, addr1, heap1) = compileExpression(env, e1, heap)
                (insts2, addr2, heap2) = compileExpression(env, e2, heap1)
                instsPlus = \
                          insts1 +\
                          insts2 +\
                          copy(addr1, 1) +\
                          copy(addr2, 2) +\
                          ["add"] +\
                          copy(0, heap2)
                return (instsPlus, heap2, heap2)
            if label == "Array":
                x = children[0]["Variable"][0]
                e = children[1]
                heap = heap + 1
                #compute the integer that the expression e represents
                (insts1, addr1, heap1) = compileExpression(env, e, heap)
                #retrieve the address a to which the environment maps the array variable x
                a = env[x]
                heap2 = heap1 + 1
                insts = insts1 +\
                        copy(addr1, 1) +\
                        ["set 2 " + str(a)] +\
                        ["add"] +\
                        copy(0, heap2) +\
                        copyFromRef(heap2, heap2+1)
                heap3 = heap2 + 1
                return (insts, heap3, heap3)
    if type(e) == Leaf:
        if e == "True":
            heap += 1
            insts = [\
                "set " + str(heap) + " 1"]
            return (insts, heap, heap)
        if e == "False":
            heap += 1
            insts = [\
                "set " + str(heap) + " 0"]
            return (insts, heap, heap)
                


def compileProgram(env, s, heap = 7): # Set initial heap default address.
    if type(s) == Leaf:
        if s == 'End':
            return (env, [], heap)

    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                [e, p] = children
                (instsE, addr, heap) = compileExpression(env, e, heap)
                (env, instsP, heap) = compileProgram(env, p, heap)
                return (env, instsE + copy(addr, 5) + instsP, heap)
            # Complete 'Assign' case for Problem #3.
            if label == "Assign":
                [v, e0, e1, e2, p] = children
                x = v["Variable"][0]
                #compute the results for all three array elements
                (instsE0, addr0, heap) = compileExpression(env, e0, heap)
                (instsE1, addr1, heap) = compileExpression(env, e1, heap)
                (instsE2, addr2, heap) = compileExpression(env, e2, heap)
                heap = heap + 1
                instsAssign = instsE0 +\
                              instsE1 +\
                              instsE2 +\
                              copy(addr0, heap) +\
                              copy(addr1, heap+1) +\
                              copy(addr2, heap+2)
                #assign the first of these three memory addresses to the variable
                env[x] = heap
                (env, instsP, heap) = compileProgram(env, p, heap+2)
                return (env, instsAssign+instsP, heap)


def compile(s):
    p = tokenizeAndParse(s)

    # Add call to type checking algorithm for Problem #5.
    # Add calls to optimization algorithms for Problem #3.
    if typeProgram({}, p) != None:
        p = foldConstants(p)
        p = unrollLoops(p)
        (env, insts, heap) = compileProgram({}, p)
        return insts
    else:
        return []

def compileAndSimulate(s):
    return simulate(compile(s))

#eof
