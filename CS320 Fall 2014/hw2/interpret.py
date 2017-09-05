#Yida Xu  xyds1522@bu.edu  U39436573  interpret.py

from math import log, floor
import re

#2.a.
def evalTerm(env, e):
    if type(e) == dict:
        for label in e:
            children = e[label]
            if label == 'Number':
                x = children[0]
                return x
                    
            elif label == 'Variable':
                x = children[0]
                if x in env:
                    return env[x]
                else:
                    print(x + ' is unbound.')
                    exit()
                    
            elif label == 'Parens':
                t = children[0]
                v = evalTerm(env, t)
                return v
            
            elif label == 'Log':
                t = children[0]
                v = evalTerm(env, t)
                return floor(log(v,2))
            
            elif label == 'Plus':
                t2 = children[1]
                v2 = evalTerm(env, t2)
                t1 = children[0]
                v1 = evalTerm(env, t1)
                return v1 + v2
            
            elif label == 'Mult':
                t2 = children[1]
                v2 = evalTerm(env, t2)
                t1 = children[0]
                v1 = evalTerm(env, t1)
                return v1 * v2

    else: return None
    

#2.b.
def evalFormula(env, e):
    if type(e) == dict:
        for label in e:
            children = e[label]
            if label == 'Variable':
                x = children[0]
                v = evalFormula(env, x)
                if x in env:
                    return env[x]
                else:
                    print(x + ' is unbound.')
                    exit()
                    
            elif label == 'Parens':
                f = children[0]
                v = evalFormula(env, f)
                return v
            
            elif label == 'Not':
                f = children[0]
                v = evalFormula(env, f)
                return not v
            
            elif label == 'Xor':
                f2 = children[1]
                v2 = evalFormula(env, f2)
                f1 = children[0]
                v1 = evalFormula(env, f1)
                return v1 != v2
            
    elif type(e) == bool:
        if e == True:
            return True
        if e == False:
            return False
        
    elif type(e) == str:
        if e == 'True':
            return True
        if e == 'False':
            return False

    else: return None
    
#3.a.
def evalEqForm(env, e):
    if type(e) == dict:
        for label in e:
            children = e[label]
            if label == 'Equal':
                x = children[0]
                y = children[1]
                v1 = evalFormula(env, x)
                v2 = evalFormula(env, y)
                if v1 != None and v2 != None:
                    return v1 == v2
    else: return None


def evalEqTerm(env, e):
    if type(e) == dict:
        for label in e:
            children = e[label]
            if label == 'Equal':
                x = children[0]
                y = children[1]
                v1 = evalTerm(env, x)
                v2 = evalTerm(env, y)
                if v1 != None and v2 != None:
                    return v1 == v2
    else: return None


def evalLessTerm(env, e):
    if type(e) == dict:
        for label in e:
            children = e[label]
            if label == 'LessThan':
                x = children[0]
                y = children[1]
                v1 = evalTerm(env, x)
                v2 = evalTerm(env, y)
                if v1 != None and v2 != None:
                    return v1 < v2
    else: return None
    
        
#2.c.
def execProgram(env, s):
    if type(s) == str:
        if s == 'End':
            return (env, [])
        
    elif type(s) == dict:
        for label in s:
            if label == 'Print':
                children = s[label]
                e = children[0]
                p = children[1]
                v = evalEqForm(env, e)
                if v == None:
                    v = evalEqTerm(env, e)
                    if v == None:
                        v = evalLessTerm(env, e)
                        if v == None:
                            v = evalFormula(env, e)
                            if v == None:
                                v = evalTerm(env, e)
                (env, o) = execProgram(env, p)
                return (env, [v] + o)
            
            if label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                e = children[1]
                p = children[2]
                v = evalEqForm(env, e)
                if v == None:
                    v = evalEqTerm(env, e)
                    if v == None:
                        v = evalLessTerm(env, e)
                        if v == None:
                            v = evalFormula(env, e)
                            if v == None:
                                v = evalTerm(env, e)
                env[x] = v        
                (env, o) = execProgram(env,p)
                return (env, o)

            if label == 'If':
                children = s[label]
                e  = children[0]
                p1 = children[1]
                p2 = children[2]
                v = evalEqForm(env, e)
                if v == None:
                    v = evalEqTerm(env, e)
                    if v == None:
                        v = evalLessTerm(env, e)
                        if v == None:
                            v = evalFormula(env, e)
                            if v == None:
                                v = evalTerm(env, e)
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
                v = evalEqForm(env, e)
                if v == None:
                    v = evalEqTerm(env, e)
                    if v == None:
                        v = evalLessTerm(env, e)
                        if v == None:
                            v = evalFormula(env, e)
                            if v == None:
                                v = evalTerm(env, e)
                    
                while v == True:
                    (env, o) = execProgram(env, p1)
                    v = evalEqForm(env, e)
                    if v == None:
                        v = evalEqTerm(env, e)
                        if v == None:
                            v = evalLessTerm(env, e)
                            if v == None:
                                v = evalFormula(env, e)
                                if v == None:
                                    v = evalTerm(env, e)
                    o2 += o

                (env, o1) = execProgram(env, p2)
                return (env, o2 + o1)

#3.b.
def execProgramExtra(env, s, assignable):
    if type(s) == str:
        if s == 'End':
            return (env, [])
        
    elif type(s) == dict:
        for label in s:
            if label == 'Print':
                children = s[label]
                e = children[0]
                p = children[1]
                v = evalEqForm(env, e)
                if v == None:
                    v = evalEqTerm(env, e)
                    if v == None:
                        v = evalLessTerm(env, e)
                        if v == None:
                            v = evalFormula(env, e)
                            if v == None:
                                v = evalTerm(env, e)
                (env, o) = execProgramExtra(env, p, assignable)
                return (env, [v] + o)
            
            if label == 'Assign':
                children = s[label]
                x = children[0]['Variable'][0]
                e = children[1]
                p = children[2]
                if x in assignable:
                    v = evalEqForm(env, e)
                    if v == None:
                        v = evalEqTerm(env, e)
                        if v == None:
                            v = evalLessTerm(env, e)
                            if v == None:
                                v = evalFormula(env, e)
                                if v == None:
                                    v = evalTerm(env, e)
                    env[x] = v
                
                (env, o) = execProgramExtra(env,p, assignable)
                return (env, o)

            if label == 'If':
                children = s[label]
                e  = children[0]
                p1 = children[1]
                p2 = children[2]
                v = evalEqForm(env, e)
                if v == None:
                    v = evalEqTerm(env, e)
                    if v == None:
                        v = evalLessTerm(env, e)
                        if v == None:
                            v = evalFormula(env, e)
                            if v == None:
                                v = evalTerm(env, e)
                if v == False:
                    (env, o1) = execProgramExtra(env, p2, assignable)
                    return (env, o1)
                elif v == True:
                    (env, o1) = execProgramExtra(env, p1, assignable)
                    (env, o2) = execProgramExtra(env, p2, assignable)
                    return (env, o1 + o2)
                
            if label == 'While':
                children = s[label]
                e  = children[0]
                p1 = children[1]
                p2 = children[2]
                o2 = []
                v = evalEqForm(env, e)
                if v == None:
                    v = evalEqTerm(env, e)
                    if v == None:
                        v = evalLessTerm(env, e)
                        if v == None:
                            v = evalFormula(env, e)
                            if v == None:
                                v = evalTerm(env, e)
                    
                while v == True:
                    (env, o) = execProgramExtra(env, p1, assignable)
                    v = evalEqForm(env, e)
                    if v == None:
                        v = evalEqTerm(env, e)
                        if v == None:
                            v = evalLessTerm(env, e)
                            if v == None:
                                v = evalFormula(env, e)
                                if v == None:
                                    v = evalTerm(env, e)
                    o2 += o

                (env, o1) = execProgramExtra(env, p2, assignable)
                return (env, o2 + o1)

#2.d.
def tokenize(syntax):
    join = r'(\s+|xor|not|\(|\)|true|false|\+|\*|log|print|assign|if|while|\;|:=|\{|\}|==|\<)'
    tokens = [t for t in re.split(join, syntax)]
    return [t for t in tokens if not t.isspace() and (not t == '')]

def interpret(s):
    tokens = tokenize(s)
    (parseTree, rest) = program(tokens)
    (env, output) = execProgramExtra({}, parseTree, assignable(parseTree))
    return output


#3.b.
def assignable(tree):
    l = assignHelp(tree)
    if l != []:
        pointer = l[0]
        u = [pointer]
        for i in l[1:]:
            if i != pointer:
                u += [i]
                poitner = i
        return u
    else:
        return []
    
def assignHelp(tree):
    if type(tree) == dict:
        for label in tree:
            if label == 'Variable':
                return tree[label]
            l = []
            for sub in tree[label]:
                l += assignHelp(sub)
            return l
    else: return []
