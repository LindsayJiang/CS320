#Linshan Jiang
#CS320 Fall 2014
#Assignment 3
#compile.py

exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('machine.py').read())

Node = dict
Leaf = str

#3.a
def compileTerm(env, t, heap):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == "Number":
                heap = heap + 1
                x = children[0]
                inst = [\
                    "set " + str(heap) + " " + str(x)]
                return (inst, heap, heap)

            if label == "Variable":
                x = children[0]
                t = env[x]
                heap = heap + 1
                inst = [\
                    "set " + str(heap) + " " + str(t)]
                #instead of returning heap as the addr, we have t as addr in this case.
                return (inst, t, heap)

            if label == "Plus":
                t1 = children[0]
                #t1 = variable x
                t2 = children[1]
                heap = heap + 1
                (insts1, addr1, heap2) = compileTerm(env, t1, heap)
                (insts2, addr2, heap3) = compileTerm(env, t2, heap2)
                instsPlus = \
                          copy(addr1, 1) +\
                          copy(addr2, 2) +\
                          ["add"] +\
                          copy(0, heap3)
                return (insts1 + insts2 + instsPlus, heap3, heap3)
            else:
                return None

#3.b
def compileFormula(env, f, heap):
    if type(f) == Leaf:
        if f == "True":
            heap = heap + 1
            inst = "set " + str(heap) + " 1"
            return ([inst], heap, heap)
        if f == "False":
            heap = heap + 1
            inst = "set " + str(heap) + " 0"
            return ([inst], heap, heap)
        else:
            return None

    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == "Variable":
                v = env[children[0]]
                heap = heap + 1
                inst = copy(v, heap)
                # the addr returned is the addr that holds the addr of variable...
                return (inst, heap, heap)
            if label == "Not":
                f1 = children[0]
                heap += 1
                (insts, addr, heap) = compileFormula(env, f1, heap)
                instsNot = \
                         ["branch setZero " + str(addr), \
                          "set " + str(heap) + " 1", \
                          "goto finish", \
                          "label setZero", \
                          "set " + str(heap) + " 0", \
                          "goto finishNot", \
                          "label finish", \
                          "set " + str(heap) + " 0", \
                          "label finishNot"]
                return (insts + instsNot, addr, heap)
            if label == "Or":
                f1 = children[0]
                f2 = children[1]
                heap = heap + 1
                (insts1, addr1, heap2) = compileFormula(env, f1, heap)
                (insts2, addr2, heap3) = compileFormula(env, f2, heap2)
                # The way of checking is add those two, and see if the result is greater than 0.
                # if greater than 0 means at least one of them is true. -> return true.
                instsOr = \
                        copy(str(addr1), 1) +\
                        copy(str(addr2), 2) +\
                        ["add", \
                         "branch setOne 0", \
                         "goto finish1", \
                         "label setOne", \
                         "set 0 1", \
                         "label finish1"] + \
                         copy(0, str(heap3))
                return (insts1 + insts2 + instsOr, heap3, heap3)

            if label == "And":
                f1 = children[0]
                f2 = children[1]
                heap = heap + 1
                (insts1, addr1, heap2) = compileFormula(env, f1, heap)
                (insts2, addr2, heap3) = compileFormula(env, f2, heap2)
                #I can't add comments inside the instsAnd as I keep getting errors
                # from the first copy to the second, I'm checking if f1 is true.
                # The way of doing this is to add 0 with it and see if the result is greater than 0
                # if mem[0] holds 1, means f1 is true, 0 otherwise.
                # Same for checking f2.
                instsAnd = \
                        copy(str(addr1), 1) +\
                        ["set 2 0", \
                         "add", \
                         "branch setOne1 0", \
                         "goto finish2", \
                         "label setOne1"] +\
                         copy(str(addr2), 1) +\
                         ["set 2 0", \
                          "add", \
                          "branch setOne2 0", \
                          "goto finish2", \
                          "label setOne2",\
                          "set 0 1",\
                          "label finish2"] +\
                          copy(0, str(heap3))
                return (insts1 + insts2 + instsAnd, heap3, heap3)

            if label == "Compare":
                f1 = children[0]
                f2 = children[1]
                heap = heap + 1
                (insts1, addr1, heap2) = compileTerm(env, f1, heap)
                (insts2, addr2, heap3) = compileTerm(env, f2, heap2)
                # the basic idea for this extra credit problem is :
                # I use addr 33333 to store the first term, keep decrement it,
                # until I get the negative of it.
                # addr 33334 stores the value everytime after decrementing.
                # then add up the two terms, and if the result equals 0, they
                # are equal. False otherwise.
                instsCompare = \
                             ["set 33333 0", \
                              "set 33334 0"] +\
                              copy(addr1, 2) +\
                              copy(2, 0)+\
                              ["branch body33333 0", \
                               "goto body222", \
                               "label body33333", \
                               "set 1 -1", \
                               "add"] +\
                              copy(0, 33334)+\
                              decrement(33333)+\
                              copy(33334,2)+\
                              ["branch body33333 33334"] +\
                              copy(addr2, 1) +\
                              copy(33333, 2)+\
                              ["add", \
                               "branch notEqual 0", \
                               "goto Equal",\
                               "label notEqual",\
                               "set 0 0", \
                               "goto finishF", \
                               "label Equal", \
                               "set 0 1",\
                               "label finishF"] +\
                               copy(0, str(heap3))
                return (insts1+insts2+instsCompare, heap3, heap3)
            else:
                return None
                                

#3.c
def compileExpression(env, s, heap):
    v = compileFormula(env, s, heap)
    if v == None:
        v = compileTerm(env, s, heap)
    return v

def compileProgram(env, s, heap):
    if type(s) == Leaf:
        if s == "End":
            return (env, [], heap)

    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == "Print":
                e = children[0]
                p = children[1]
                heap = heap + 1
                (insts1, addr, heap1) = compileExpression(env, e, heap)
                (env2, insts2, heap2) = compileProgram(env, p, heap1)
                # copy result to addr5 -> defult addr for printing.
                return (env2, insts1 + copy(addr, 5) + insts2, heap2)

            if label == "If":
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                heap = heap + 1
                (insts1, addr, heap1) = compileExpression(env, e, heap)
                (env2, insts2, heap2) = compileProgram(env, p1, heap1)
                (env3, insts3, heap3) = compileProgram(env2, p2, heap2)
                instsIf = \
                        insts1 +\
                        ["branch body " + str(addr),\
                         "goto finish3", \
                         "label body"] + \
                         insts2 +\
                         ["label finish3"] +\
                         insts3
                return (env3, instsIf, heap3)

            if label == "While":
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                heap = heap + 1
                (insts1, addr, heap1) = compileExpression(env, e, heap)
                (env2, insts2, heap2) = compileProgram(env, p1, heap1)
                (env3, insts3, heap3) = compileProgram(env2, p2, heap2)
                instsWhile = \
                           insts1 +\
                           ["label start", \
                            "branch body1 " + str(addr),\
                            "goto finish4", \
                            "laebl body1"] +\
                            insts2 +\
                            ["goto start",\
                            "label finish4"] +\
                            insts3
                return (env3, instsWhile, heap3)

            if label == "Assign":
                x = children[0]["Variable"][0]
                e = children[1]
                p = children[2]
                heap = heap + 1
                (insts1, addr, heap1) = compileExpression(env, e, heap)
                # the x is assgined to the addr that holds the addr of x...
                env[x] = addr
                (env2, insts2, heap2) = compileProgram(env, p, heap1)
                return (env2, insts1 + insts2, heap2)

            if label == "Procedure":
                x = children[0]["Variable"][0]
                p1 = children[1]
                p2 = children[2]
                heap = heap + 1
                (env2, insts2, heap1) = compileProgram(env, p1, heap)
                (env3, insts3, heap2) = compileProgram(env2, p2, heap1)
                return (env2, procedure(x, insts2) + insts3, heap2)

            if label == "Call":
                x = children[0]["Variable"][0]
                p2 = children[1]
                heap = heap + 1
                (env2, insts2, heap1) = compileProgram(env, p2, heap)
                return (env2, call(x) + insts2, heap1)
            else:
                return None
            
#3.d
def compile(s):
    Tree = tokenizeAndParse(s)
    (env, insts, heap) = compileProgram({}, Tree, 8)
    return \
           ["set 7 -1", \
            "set -1 0"] +\
            insts
            
                
            
