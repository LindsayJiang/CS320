######################################################################
# Linshan Jiang
# CAS CS 320, Spring 2015
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
            if label == "Number":
                x = children[0]
                return x
            elif label == "Variable":
                x = children[0]
                if x in env:
                    t = env[x]
                    return t
                else:
                    print(x + ' is unbound.')
                    exit()
            elif label == "Plus":
                t1 = children[1]
                v1 = evalTerm(env, t1)
                t2 = children[0]
                v2 = evalTerm(env, t2)
                return v1 + v2
            else:
                return None
    else:
        return None

def evalFormula(env, f):
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == "Variable":
                x = children[0]
                if x in env:
                    v = env[x]
                    return v
                else:
                    print(x + ' is unbound.')
                    exit()
            elif label == "Not":
                x = children[0]
                v = evalFormula(env, x)
                if v == "True":
                    return "False"
                else:
                    return "True"
                
            elif label == "And":
                f1 = children[0]
                v1 = evalFormula(env, f1)
                #And-Short
                if v1 == "False":
                    return "False"
                else:
                    #And
                    f2 = children[1]
                    v2 = evalFormula(env, f2)
                    if v2 == "True":
                        return "True"
                    else:
                        return "False"
            elif label == "Or":
                f1 = children[0]
                v1 = evalFormula(env, f1)
                #Or-short
                if v1 == "True":
                    return "True"
                #Or
                else:
                    f2 = children[0]
                    v2 = evalFormula(env, f2)
                    if v2 == "False":
                        return "False"
                    else:
                        return "True"

            elif label == "Compare":
                f1 = children[0]
                v1 = evalTerm(env, f1)
                f2 = children[1]
                v2 = evalTerm(env, f2)
                if v1 == v2:
                    return "True"
                else:
                    return "False"

                
    elif type(f) == Leaf:
        if f == "True":
            return "True"
        elif f == "False":
            return "False"
                

def evalExpression(env, e): # Useful helper function.
    v = evalTerm(env, e)
    if v == None:
        v = evalFormula(env, e)
    return v


def execProgram(env, s, oRest = []):
    if type(s) == Leaf:
        if s == "End":
            return (env, [])
        else:
            return None
    
    elif type(s) == Node:
        for label in s:
            if label == "Print":
                children = s[label]
                e = children[0]
                p = children[1]
                #Here I check both evalTerm and evalFormula as they both contains "Print".
                v = evalTerm(env, e)
                if v == None:
                    v = evalFormula(env, e)
                (env2, o) = execProgram(env, p)
                return (env2, [v] + o)
            elif label == "If":
                children = s[label]
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                v = evalTerm(env, e)
                if v == None:
                    v = evalFormula(env, e)
                if v == "False":
                    (env2, o1) = execProgram(env, p2)
                    return (env2, o1)
                elif v == "True":
                    (env2, o1) = execProgram(env, p1)
                    (env3, o2) = execProgram(env2, p2)
                    return (env, o1 + o2)

            elif label == "While":
                children = s[label]
                e = children[0]
                p1 = children[1]
                p2 = children[2]
                v = evalTerm(env, e)
                
                if v == None:
                    v = evalFormula(env, e)
                #if false, just do it once.
                if v == "False":
                    (env, o) = execProgram(env, p2, oRest)
                    oRest = oRest + o
                    return (env, oRest)
                #if v == "True"
                else:
                    (env, o) = execProgram(env, p1, oRest)
                    oRest = oRest + o
                    v = evalTerm(env, e)
                    if v == "False":
                        (env, o) = execProgram(env, p2, oRest)
                        oRest += o
                    elif v == "True":
                        (env, o) = execProgram(env, p1, oRest)
                        oRest += o
                    return (env, oRest)
            elif label == "Assign":
                children = s[label]
                x = children[0]["Variable"][0]
                e = children[1]
                p = children[2]
                v = evalTerm(env, e)
                if v == None:
                    v = evalFormula(env, e)
                env[x] = v
                (env2, o) = execProgram(env, p)
                return (env2, o)

            elif label == "Procedure":
                children = s[label]
                x = children[0]["Variable"][0]
                p1 = children[1]
                p2 = children[2]
                env[x] = p1
                (env2, o) = execProgram(env, p2)
                return (env2, o)

            elif label == "Call":
                children = s[label]
                x = children[0]["Variable"][0]
                p2 = children[1]
                if x in env:
                    p1 = env[x]
                    (env2, o1) = execProgram(env, p1)
                    (env3, o2) = execProgram(env2, p2)
                    return (env3, o1 + o2)

            elif label == "End":
                return (env, [])
        
            else:
                return None
    else:
        return None
                    
def interpret(s):
    (env, o) = execProgram({}, tokenizeAndParse(s))
    return o

#eof
