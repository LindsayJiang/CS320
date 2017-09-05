#Linshan Jiang (U67862687)
#interpret

import re

#2.a. / 3.
#added compare, lessThan and greaterThan for extra credit
def evalTerm(env, t):
    Node = dict
    Leaf = bool

    if type(t) == Node:
        for label in t:
            children = t[label]
            if label == "Number":
                x = children[0]
                return x

            elif label == "Variable":
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()

            elif label == "Parens":
                t = children[0]
                v = evalTerm(env, t)
                return v

            elif label == "Int":
                t = children[0]
                if evalTerm(env, t) == "True":
                    return ({'Number': [1]})
                elif evalTerm(env, t) == "False":
                    return ({'Number': [0]})

            elif label == "Add":
                t1 = children[0]
                v1 = evalTerm(env, t1)
                t2 = children[1]
                v2 = evalTerm(env, t2)
                return (v1 + v2)

            elif label == "Multiply":
                t1 = children[0]
                v1 = evalTerm(env, t1)
                t2 = children[1]
                v2 = evalTerm(env, t2)
                return (v1 * v2)

            elif label == "Compare":
                t1 = children[0]
                v1 = evalTerm(env, t1)
                t2 = children[1]
                v2 = evalTerm(env, t2)
                if v1 == v2:
                    return "True"
                else:
                    return "False"

            elif label == "LessThan":
                t1 = children[0]
                v1 = evalTerm(env, t1)
                t2 = children[1]
                v2 = evalTerm(env, t2)
                if v1 < v2:
                    return "True"
                else:
                    return "False"

            elif label == "GreaterThan":
                t1 = children[0]
                v1 = evalTerm(env, t1)
                t2 = children[1]
                v2 = evalTerm(env, t2)
                if v1 > v2:
                    return "True"
                else:
                    return "False"
            else:
                return None

    else:
        return None

#2.b.        
def evalFormula(env, f):
    Node = dict
    Leaf = bool
    
    if type(f) == Node:
        for label in f:
            children = f[label]
            if label == "Variable":
                x = children[0]
                v = evalFormula(env, x)
                if x in env:
                    return env[x]
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == "Bool":
                f = children[0]
                v = evalFormula(env, f)
                if v != 0:
                    return "True"
                elif v == 0:
                    return "False"

            elif label == "Xor":
                f1 = children[0]
                v1 = evalFormula(env, f1)
                f2 = children[1]
                v2 = evalFormula(env, f2)
                if v1 != v2:
                    return "True"
                else:
                    return "False"
            else:
                return None

    elif type(f) == str:
        if f == "True":
            return "True"
        elif f == "False":
            return "False"
        else:
            return None

    elif type(f) == Leaf:
        if f == True:
            return "True"
        elif f == False:
            return "False"

    else:
        return None

#2.c.
def execProgram(env, s, oRest=[]):
    Node = dict
    Leaf = str

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

            elif label == "Assign":
                children = s[label]
                x = children[0]["Variable"][0]
                e = children[1]
                p = children[2]
                #Here I check both evalTerm and evalFormula as they both contains "Print".
                v = evalTerm(env, e)
                if v == None:
                    v = evalFormula(env, e)
                env[x] = v
                (env2, o) = execProgram(env, p)
                return (env2, o)

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
            elif label == "End":
                return (env, [])
        
            else:
                return None
        else:
            return None

def interpret(string):
    #tokenize the string
    terminals = "(\s+|xor|bool|\(|\)|true|false|\+|\*|int|print|\;|assign|\=|if|\{|\}|while|\<|\>)"
    tokens = [t for t in re.split(terminals, string)]
    tokens = [t for t in tokens if not t.isspace() and (not t == '')]
    (parseTree, rest) = program(tokens)
    if not parseTree == None:
        r = execProgram({}, parseTree)
        if not r == None:
            (env, output) = r
            return output
    else:
        return None


