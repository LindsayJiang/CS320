#####################################################################
#
# CAS CS 320, Spring 2015
# Midterm (skeleton code)
# analyze.py
# Linshan Jiang (linshan@bu.edu)
#
#  ****************************************************************
#  *************** Modify this file for Problem #5. ***************
#  ****************************************************************
#

exec(open("parse.py").read())

Node = dict
Leaf = str

def typeExpression(env, e):
    if type(e) == Leaf:
        # Complete base cases for booleans for Problem #4.
        if e == "True" or e == "False":
            return "Boolean"


    if type(e) == Node:
        for label in e:
            children = e[label]
            if label == 'Number':
                return 'Number'

            if label == 'Variable':
                # Complete case for 'Variable' for Problem #4.
                x = children[0]
                if env[x] == "Number":
                    return "Number"

            elif label == 'Array':
                [x, e] = children
                x = x['Variable'][0]
                if x in env and env[x] == 'Array' and typeExpression(env, e) == 'Number':
                    return 'Number'

            elif label == 'Plus':
                # Complete case for 'Plus' for Problem #4.
                [e1, e2] = children
                if typeExpression(env, e1) == "Number" and typeExpression(env, e2) == "Number":
                    return "Number"
                
def typeProgram(env, s):
    if type(s) == Leaf:
        if s == 'End':
            return 'Void'
    elif type(s) == Node:
        for label in s:
            if label == 'Print':
                [e, p] = s[label]
                # Complete case(s) for 'Print' for Problem #4.
                t1 = typeExpression(env, e)
                t2 = typeProgram(env, p)
                if t2 == "Void" and t1 == "Boolean":
                    return "Void"
                if t2 == "Void" and t1 == "Number":
                    return "Void"

            if label == 'Assign':
                [x, e0, e1, e2, p] = s[label]
                x = x['Variable'][0]
                if typeExpression(env, e0) == 'Number' and\
                   typeExpression(env, e1) == 'Number' and\
                   typeExpression(env, e2) == 'Number':
                     env[x] = 'Array'
                     if typeProgram(env, p) == 'Void':
                           return 'Void'

            if label == 'For':
                [x, p1, p2] = s[label]
                x = x['Variable'][0]
                # Complete case for 'For' for Problem #4.
                env[x] = "Number"
                if typeProgram(env, p2) == "Void":
                    env[x] = "Number"
                    if typeProgram(env, p1) == "Void":
                        return "Void"

#eof
