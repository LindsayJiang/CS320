#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3
# compile.py
#

exec(open('parse.py').read())
exec(open('interpret.py').read())
exec(open('machine.py').read())

Node = dict
Leaf = str


#3.a.
def compileTerm(env, t, heap):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Number':
                heap += 1
                inst = \
                     ['set ' + str(heap) + ' ' + str(children[0]) \
                      ]
                return (inst, heap, heap)

            if label == 'Variable':
                v = env[children[0]]
                heap += 1
                inst = copy(v, heap)
                return (inst, heap, heap)

            if label == 'Plus':
                t1 = children[0]
                t2 = children[1]
                heap += 1
                (insts1, addr1, heap2) = compileTerm(env, t1, heap)
                (insts2, addr2, heap3) = compileTerm(env, t2, heap2)
                instsPlus = \
                            insts1 + \
                            insts2 + \
                            copy(addr1, 1) + \
                            copy(addr2, 2) + \
                            ['add'] + \
                            copy(0, heap3)
                return (instsPlus, heap3, heap3)


#3.b.
def compileFormula(env, f, heap):
    if type(f) == Leaf:
        if f == 'True':
            heap += 1
            inst = 'set ' + str(heap) + ' 1'
            return ([inst], heap, heap)
        if f == 'False':
            heap += 1
            inst = 'set ' + str(heap) + ' 0'
            return ([inst], heap, heap)

    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Variable':
                v = env[children[0]]
                heap += 1
                inst = copy(v, heap)
                return (inst, heap, heap)
            
            if label == 'Not':
                f1 = children[0]
                heap += 1
                (insts, addr, heap) = compileFormula(env, f1, heap)
                instsNot = \
                         ['brach setZero200 ' + str(heap), \
                          'set ' + str(heap) + ' 1', \
                          'goto finish200', \
                          'label setZero200', \
                          'set ' + str(heap) + ' 0', \
                          'goto finishNot200', \
                          'label finish200', \
                          'set ' + str(heap) + ' 0', \
                          'label finishNot200' \
                          ]
                return (insts + instsNot, heap, heap)
            
            if label == 'Or':
                f1 = children[0]
                f2 = children[1]
                heap += 1
                (insts1, addr1, heap2) = compileFormula(env, f1, heap)
                (insts2, addr2, heap3) = compileFormula(env, f2, heap2)
                instsOr = \
                        copy(str(heap2), 1) + \
                        copy(str(heap3), 2) + \
                        ['add', \
                         'branch setOne250 0', \
                         'goto finish250', \
                         'label setOne250', \
                         'set 0 1', \
                         'label finish250'] + \
                        copy(0, str(heap3))
                return (insts1 + insts2 + instsOr, heap3, heap3)

            if label == 'And':
                f1 = children[0]
                f2 = children[1]
                heap += 1
                (insts1, addr1, heap2) = compileFormula(env, f1, heap)
                (insts2, addr2, heap3) = compileFormula(env, f2, heap2)
                instsAnd = \
                         copy(str(heap2), 1) + \
                         ['set 2 0', \
                          'add', \
                          'branch setOne300 0', \
                          'goto finish300', \
                          'label setOne300'] + \
                         copy(str(heap3), 1) + \
                         ['set 2 0', \
                          'add', \
                          'branch setOne350 0', \
                          'goto finish300', \
                          'label setOne350', \
                          'set 0 1', \
                          'label finish300'] + \
                         copy(0, str(heap3))
                return (insts1 + insts2 + instsAnd, heap3, heap3)


#3.c.
def compileExpression(env, s, heap):
    e = compileFormula(env, s, heap)
    if not e == None:
        return e
    return compileTerm(env, s, heap)


def compileProgram(env, s, heap):
    if type(s) == Leaf:
        if s == 'End':
            return (env, [], heap)

    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == 'Print':
                e = children[0]
                p = children[1]
                heap += 1
                (insts1, addr1, heap2) = compileExpression(env, e, heap)
                (env2, insts2, heap3) = compileProgram(env, p, heap2)
                return (env2, insts1 + copy(addr1, 5) + insts2 , heap3)

            if label == 'Assign':
                v = children[0]['Variable'][0]
                e = children[1]
                p = children[2]
                heap += 1
                (insts1, addr1, heap2) = compileExpression(env, e, heap)
                env[v] = addr1
                (env2, insts2, heap3) = compileProgram(env, p, heap2)
                return (env2, insts1 + insts2, heap3)

            if label == 'If':
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                heap += 1
                (insts1, addr1, heap2) = compileExpression(env, e, heap)
                (env2, insts2, heap3) = compileProgram(env, p1, heap2)
                (env3, insts3, heap4) = compileProgram(env2, p2, heap3)
                instsIf = \
                        insts1 + \
                        ['branch body100 ' + str(addr1), \
                         'goto finish100', \
                         'label body100'] + \
                        insts2 + \
                        ['label finish100'] + \
                        insts3
                return (env3, instsIf, heap4)

            if label == 'While':
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                heap += 1
                (insts1, addr1, heap2) = compileExpression(env, e, heap)
                (env2, insts2, heap3) = compileProgram(env, p1, heap2)
                (env3, insts3, heap4) = compileProgram(env2, p2, heap3)
                instsWhile = \
                           insts1 + \
                           ['label whileStart200', \
                            'branch body200 ' + str(addr1), \
                            'goto finishWhile200', \
                            'label body200'] + \
                            insts2 + \
                            ['goto whileStart200', \
                             'label finishWhile200'] + \
                            insts3
                return (env3, instsWhile, heap4)

            if label == 'Procedure':
                v = children[0]['Variable'][0]
                p1 = children[1]
                p2 = children[2]
                heap += 1
                (env2, insts1, heap2) = compileProgram(env, p1, heap)
                (env3, insts2, heap3) = compileProgram(env2, p2, heap2)
                return (env3, procedure(v, insts1) + insts2, heap3)

            if label == 'Call':
                v = children[0]['Variable'][0]
                p = children[1]
                heap += 1
                (env2, insts1, heap2) = compileProgram(env, p, heap)
                return (env2, call(v) + insts1, heap2)


#3.d.
def compile(s):
    p = tokenizeAndParse(s)
    (env, insts, heap) = compileProgram({}, p, 7)
    return \
           ['set -1 0', \
            'set 7 -1'] + \
            insts

#eof
