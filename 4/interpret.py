#####################################################################
#
# CAS CS 320, Spring 2015
# Assignment 4 (skeleton code)
# Linshan Jiang (linshan@bu.edu)
# interpret.py
#

exec(open("parse.py").read())

def subst(s, a):
    # Complete for Problem #1, part (a).

    #this is the base case.
    if "Variable" in a:
        #variable to be substituted.
        x = a["Variable"][0]
        #if there is a substitution, we substitute it, else, a is not changed
        if x in s:
            a = s[x]
        return a
    #recursive case
    for label in a:
        children = a[label]
        for aPrime in range(len(children)):
            children[aPrime] = subst(s, children[aPrime])
    return a

def unify(a, b):
    # Complete for Problem #1, part (b).

    #if both a and b are leaf nodes and are equivalent
    if (type(a) != dict) and (type(b) != dict) and (a == b):
        return {}
    #if a is a variable node representing a variable x
    if 'Variable' in a:
        x = a['Variable'][0]
        return {x: b}
    #if b is a variable node representing a variable x
    if 'Variable' in b:
        x = b['Variable'][0]
        return {x: a}
    
    if type(a) == dict and type(b) == dict:
        subst = {}
        for labelA in a:
            for labelB in b:
                #if both a and b have the same label and the same number of children
                if (labelA == labelB) and (len(a[labelA]) == len(b[labelB])):
                    for i in range(len(a[labelA])):
                        afterUnity = unify(a[labelA][i], b[labelB][i])
                        if afterUnity == None:
                            return None
                        else:
                            subst.update(afterUnity)
                else:
                    return None

        return subst
    else:
        return None


def build(m, d):
    # Complete for Problem #2, part (a).
    if d == "End":
        return m
    else:
        for label in d:
            if label == "Function":
                children = d[label]
                f = children[0]["Variable"][0]
                p = children[1]
                e = children[2]
                d1 = children[3]
                # declaration function first case
                if not (f in m):
                    m.update({f:[(p, e)]})
                # declaration function more case
                elif f in m:
                    m[f].append((p, e))
                return build(m, d1)
  
def evaluate(m, env, e):
    # Complete for Problem #2, part (b).
    if type(e) == dict:
        for label in e:
            children = e[label]
            if label == "ConInd":
                c = children[0]
                e1 = children[1]
                e2 = children[2]
                v1 = evaluate(m, env, e1)
                v2 = evaluate(m, env, e2)
                return {"ConInd": [c, v1, v2]}
            elif label == "ConBase":
                c = children[0]
                return e
            elif label == "Number":
                n = children[0]
                return n
            elif label == "Variable":
                x = children[0]
                v = env[x]
                return v
            elif label == "Plus":
                e1 = children[0]
                e2 = children[1]
                n1 = evaluate(m, env, e1)
                n2 = evaluate(m, env, e2)
                return n1 + n2
            elif label == "Apply":
                f = children[0]["Variable"][0]
                e1 = children[1]
                v1 = evaluate(m, env, e1)
                for tuples in m[f]:
                    (p, e2) = tuples
                    s = unify(p, v1)
                    if s != None:
                        env.update(s)
                        v2 = evaluate(m, env, e2)
                        return v2
            else:
                return None
    else:
        return e

def interact(s):
    # Build the module definition.
    m = build({}, parser(grammar, 'declaration')(s))

    # Interactive loop.
    while True:
        # Prompt the user for a query.
        s = input('> ') 
        if s == ':quit':
            break
        
        # Parse and evaluate the query.
        e = parser(grammar, 'expression')(s)
        if not e is None:
            print(evaluate(m, {}, e))
        else:
            print("Unknown input.")

#eof
