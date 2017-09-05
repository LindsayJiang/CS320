#####################################################################
#
# CAS CS 320, Fall 2014
# Assignment 4
# Yida Xu  xyds1522@bu.edu  U39436573
# interpret.py
#

exec(open("parse.py").read())

def subst(s, a):
    if 'Variable' in a:
        x = a['Variable'][0]
        if x in s:
            a = s[x]
        return a
    else:
        for label in a:
            children = a[label]
            for i in range(0, len(children)):
                children[i] = subst(s, children[i])
        return a
            

def unify(a, b):
    if type(a) != dict and type(b) != dict and a == b:
        return {}
    if 'Variable' in a:
        x = a['Variable'][0]
        return {x: b}
    if 'Variable' in b:
        x = b['Variable'][0]
        return {x: a}
    subs = {}
    for labela in a:
        for labelb in b:
            if (labela == labelb) and (len(a[labela]) == len(b[labelb])):
                for i in range(0, len(a[labela])):
                    subs.update(unify(a[labela][i], b[labelb][i]).items())
    return subs


def build(m, d):
    if type(d) != dict and d == 'End':
        return m
    else:
        for label in d:
            if label == 'Function':
                children = d[label]
                f = children[0]['Variable'][0]
                p = children[1]
                e = children[2]
                r = children[3]
                if f not in m:
                    print("f not in m; f = ", f, "m = ", m)
                    m[f] = [(p, e)]
                    print("m after = ", m)
                elif f in m:
                    print("f in m; f = ", f, "m =", m)
                    m[f].append((p, e))
                    print("m after = ", m)
                return build(m, r)
            
                    
def evaluate(m, env, e):
    if type(e) == dict:
        for label in e:
            if label == 'Apply':
                children = e[label]
                f = children[0]['Variable'][0]
                e1 = children[1]
                v1 = evaluate(m, env, e1)
                for t in m[f]:
                    (p, e2) = t
                    if p == v1:
                        env.update(m)
                v2 = evaluate(m, env, e2)
                return v2
            
            elif label == 'Variable':
                children = e[label]
                x = children[0]
                return env[x]
            
            elif label == 'Plus':
                children = e[label]
                e1 = children[0]
                e2 = children[1]
                n1 = evaluate(m, env, e1)
                n2 = evaluate(m, env, e2)
                return n1 + n2
            
            elif label == 'Constructor':
                children = e[label]
                if len(children) == 1:
                    c = children[0]
                    return c
                elif len(children) == 3:
                    c = children[0]
                    e1 = children[1]
                    e2 = children[2]
                    v1 = evaluate(m, env, e1)
                    v2 = evaluate(m, env, e2)
                    return (c, v1, v2)
                
            else:
                return e
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
