#####################################################################
#
# CAS CS 320, Spring 2015
# Midterm (skeleton code)
# interpret.py
# Linshan jiang(linshan@bu.edu)
#  ****************************************************************
#  *************** Modify this file for Problem #2. ***************
#  ****************************************************************
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def evaluate(env, e):
    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == "Number":
                n = children[0]
                return n
            elif label == "Variable":
                x = children[0]
                if x in env:
                    n = env[x]
                    return n
                else:
                    print(x + " is unbound.")
                    exit()
            elif label == "Plus":
                e1 = children[0]
                n1 = evaluate(env, e1)
                e2 = children[1]
                n2 = evaluate(env, e2)
                return n1 + n2
            elif label == "Array":
                x = children[0]["Variable"][0]
                e = children[1]
                [n1, n2, n3] = env[x]
                k = evaluate(env, e)
                if k == "True" or k == "False":
                    k = bool(k)
                if k >= 0 and k <= 2:
                    return [n1, n2, n3][k]
    elif type(e) == Leaf:
        if e == "True":
            return "True"
        elif e == "False":
            return "False"
    else:
        return None
    # Complete for Problem #2.

def execute(env, s):
    if type(s) == Node:
        for label in s:
            children = s[label]
            if label == "Assign":
                x = children[0]["Variable"][0]
                e0 = children[1]
                e1 = children[2]
                e2 = children[3]
                p = children[4]
                n0 = evaluate(env, e0)
                n1 = evaluate(env, e1)
                n2 = evaluate(env, e2)
                env[x] = [n0, n1, n2]
                (env1, o) = execute(env, p)
                return (env1, o)
            elif label == "Print":
                e = children[0]
                p = children[1]
                v = evaluate(env, e)
                (env2, o) = execute(env, p)
                return (env2, [v] + o)
            elif label == "For":
                x = children[0]["Variable"][0]
                p1 = children[1]
                p2 = children[2]
                env[x] = 0
                (env2, o1) = execute(env, p1)
                env2[x] = 1
                (env3, o2) = execute(env2, p1)
                env3[x] = 2
                (env4, o3) = execute(env3, p1)
                (env5, o4) = execute(env4, p2)
                return (env5, o1 + o2 + o3 + o4)
    elif type(s) == Leaf:
        if s == "End":
            return (env, [])
                
    # Complete for Problem #2.

def interpret(s):
    # Complete for Problem #2.
    (env, o) = execute({}, tokenizeAndParse(s))
    return o


#eof
