# Yida Xu  xyds1522@bu.edu  CS320 hw1

import re

#1.a.
def tokenize(terminals, syntax):
    join = '(\s+'
    for i in terminals:
        if i == '+' or i == '*' or i == '(' or i == ')' or i == ';':
            join += ('|' + '\\' + i)
        elif i == '||' or i == '==':
            join += ('|' + '\\' + i[0] + '\\' + i[1])
        else:
            join += ('|' + i)
    join += ')'
    print(join)
    tokens = [t for t in re.split(join, syntax)]
    return [t for t in tokens if not t.isspace() and (not t == '')]


#1.b.
def directions(tokens):
    if tokens[0] == 'forward' and tokens[1] == ';':
        (e1, tokens) = directions(tokens[2:])
        return ({'Forward': [e1]}, tokens)

    if tokens[0] == 'reverse' and tokens[1] == ';':
        (e1, tokens) = directions(tokens[2:])
        return ({'Reverse': [e1]}, tokens)

    if tokens[0] == 'left' and tokens[1] == 'turn' and tokens[2] == ';':
        (e1, tokens) = directions(tokens[3:])
        return ({'LeftTurn': [e1]}, tokens)

    if tokens[0] == 'right' and tokens[1] == 'turn' and tokens[2] == ';':
        (e1, tokens) = directions(tokens[3:])
        return ({'RightTurn': [e1]}, tokens)

    if tokens[0] == 'stop' and tokens[1] == ';':
        return ('Stop', tokens[2:])


#2.number()
def number(tokens):
    if re.match(r"^([1-9][0-9]*)$", tokens[0]):
        return (int(tokens[0]), tokens[1:])
         
    
#2.a.
def variable(tokens):
    if re.match("^[a-zA-Z]+$", tokens[0]):
        return (tokens[0], tokens[1:])

def variableLabel(tokens):
    if re.match("^[a-zA-Z]+$", tokens[0]):
        return ({"Variable": [tokens[0]]}, tokens[1:])

#2.b.
#3.
def term(tmp, top=True):
    seqs = [\
        ('Plus', ['plus', '(', term, ',', term, ')']), \
        ('Mult', ['mult', '(', term, ',', term, ')']), \
        ('Log', ['log', '(', term, ')']), \
        ('Variable', ['@', variable]), \
        ('Number', ['#', number]), \
        ('Plus', ['(', term, '+', term, ')']), \
        ('Mult', ['(', term, '*', term, ')']) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []

        for x in seq:
            if type(x) == type(""):
                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break
            else:
                if x.__name__ == "variable" or x.__name__ == "number":
                    r = x(tokens)
                else:
                    r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)


#2.c.
#3.
def formula(tmp, top):
    seqs = [\
        ('True', ['true']), \
        ('False', ['false']), \
        ('Not', ['not', '(', formula, ')']), \
        ('And', ['and', '(', formula, ',', formula, ')']), \
        ('Or', ['or', '(', formula, ',', formula, ')']), \
        ('Equal', ['(', term, '==', term, ')']), \
        ('Equal', ['equal', '(', term, ',', term, ')']), \
        ('LessThan', ['less', 'than', '(', term, ',', term, ')']), \
        ('GreaterThan', ['greater', 'than', '(', term, ',', term, ')']), \
        ('GreaterThan', ['(', term, '>', term, ')']), \
        ('LessThan', ['(', term, '<', term, ')']), \
        ('And', ['(', formula, '&&', formula, ')']), \
        ('Or', ['(', formula, '||', formula, ')']) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []

        for x in seq:
            if type(x) == type(""):
                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break

            else:
                r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)
                            


#2.d.
def program(tmp, top):
    seqs = [\
        ('Print',  ['print', formula, ';', program]), \
        ('Print',  ['print', term, ';', program]), \
        ('Assign', ['assign', '@', variableLabel, ':=', term, ';', program]), \
        ('End',    ['end', ';']) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []
        for x in seq:
            if type(x) == type(""):
                if tokens[0] == x:
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break
                
            else:
                if x.__name__ == "variableLabel":
                    r = x(tokens)
                else:
                    r = x(tokens, False)
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]
                    
        if len(ss)+ len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)


#2.e.
def complete(tokens):
    allTerminals = ['print', ';', 'assign', '@', ':=', 'end', 'true', 'false', \
                'not', '(', ')', 'and', ',', 'or', 'equal', 'less', 'than', '*', \
                'greater', 'plus', 'mult', 'log', '#', '||', '&&', '==', '>', '<']
    
    tokens = str(tokens)
    tokens = tokenize(allTerminals, tokens)
    
    if tokens[0] == 'print' or tokens[0] == 'assign' or tokens[0] == 'end':
        (tree, left) = program(tokens, True)
        return tree
        
    elif tokens[0] == 'true' or tokens[0] == 'false' or tokens[0] == 'not' \
       or tokens[0] == 'and' or tokens[0] == 'or' or tokens[0] == 'equal' \
       or tokens[0] == 'less' or tokens[0] == 'greater':
        (tree, left) = formula(tokens, True)
        return tree
        
    elif tokens[0] == 'plus' or tokens[0] == 'mult' or tokens[0] == 'log' \
       or tokens[0] == '@' or tokens[0] == '#':
        (tree, left) = term(tokens, True)
        return tree

    elif tokens[0] == '(':
        (tree, left) = formula(tokens)
        if not left is None:
            (tree, left) = term(tokens)
        return (tree, left)
