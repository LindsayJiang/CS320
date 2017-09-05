######################################################################
#
# CAS CS 320, Fall 2014
# Assignment 3
# interpret.py
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def evalTerm(env, t):
    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == 'Number':
                x = children[0]
                return x

            elif label == 'Variable':
                x = children[0]                
                if x in env:
                    t = env[x]
                    return evalTerm(env, t)
                else:
                    print(x + ' is unbound.')
                    exit()

            elif label == 'Plus':
                t2 = children[1]
                v2 = evalTerm(env, t2)
                t1 = children[0]
                v1 = evalTerm(env, t1)
                return v1 + v2
            
    else: return None


#1.b.
def evalFormula(env, f):
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == 'Variable':
                x = children[0]
                if x in env:
                    f = env[x]
                    return evalFormula(env, f)
                else:
                    print(x + ' is unbound.')
                    exit()
                    
            elif label == 'Not':
                f = children[0]
                v = evalFormula(env, f)
                return not v

            elif label == 'And':
                f2 = children[1]
                v2 = evalFormula(env, f2)
                f1 = children[0]
                v1 = evalFormula(env, f1)
                return v1 and v2

            elif label == 'Or':
                f2 = children[1]
                v2 = evalFormula(env, f2)
                f1 = children[0]
                v1 = evalFormula(env, f1)
                return v1 or v2

    if type(f) == Leaf:
        if f == 'True':
            return True
        if f == 'False':
            return False
        

#1.c.
def execProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return (env, [])

    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                children = s[label]
                e = children[0]
                p = children[1]
                v = evalTerm(env, e)
                if v == None:
                    v = evalFormula(env, e)
                (env, o) = execProgram(env, p)
                return (env, [v] + o)

            if label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                e = children[1]
                p = children[2]
                env[x] = e
                (env, o) = execProgram(env, p)
                return (env, o)

            if label == 'If':
                children = s[label]
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                v = evalTerm(env, e)
                if v == None:
                    v = evalFormula(env, e)
                if v == False:
                    (env, o1) = execProgram(env, p2)
                    return (env, o1)
                elif v == True:
                    (env, o1) = execProgram(env, p1)
                    (env, o2) = execProgram(env, p2)
                    return (env, o1 + o2)

            if label == 'While':
                children = s[label]
                e  = children[0]
                p1 = children[1]
                p2 = children[2]
                o2 = []
                v = evalTerm(env, e)
                if v == None:
                    v = evalFormula(env, e)

                while v == True:
                    (env, o) = execProgram(env, p1)
                    v = evalTerm(env, s)
                    if v == None:
                        v = evalFormula(env, e)
                    o2 += o
                (env, o1) = execProgram(env, p2)
                return (env, o2 + o1)

            if label == 'Procedure':
                children = s[label]
                x = children[0]['Variable'][0]
                p1 = children[1]
                p2 = children[2]
                env[x] = p1
                (env, o) = execProgram(env, p2)
                return (env, o)

            if label == 'Call':
                children = s[label]
                x = children[0]['Variable'][0]
                p2 = children[1]
                p1 = env[x]
                (env, o1) = execProgram(env, p1)
                (env, o2) = execProgram(env, p2)
                return (env, o1 + o2)


def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o

#eof
