#Linshan Jiang (linshan@bu.edu)
#hw2 parse.py

import re

#1.a.
def number(tokens):
    if re.match(r"^([1-9][0-9]*|[0]|[1-9]?)$", tokens[0]):
        return (int(tokens[0]), tokens[1:])
    else:
        return None

def variable(tokens):
    #to avoid this function consume "true" or "false"
    if (not tokens[0] == "true") and (not tokens[0] == "false"):
        if re.match(r"^([a-z]+[a-z,A-Z,0-9]*)$", tokens[0]):
            return (tokens[0], tokens[1:])
    return None

#1.b. / #3.
#added compare, lessThan, and greaterThan for extra credit cases.
def formula(tokens,top = True):
    #included top flag
    if top == False:
        (e1, tokens) = leftFormula(tokens, False)
        #check if it is xor case by checking the remaining of tokens
        if not (e1 == None) and (not tokens == []):
            #if next token is xor, then it must conform to the grammar.
            if tokens[0] == "xor":
                (e2, tokens) = formula(tokens[1:],False)
                if not e2 == None:
                    return ({"Xor":[e1, e2]}, tokens)
                else:
                    return None
            #here is the difference between top False and True. Instead of returning
            #None, I should return the remaining of tokens.
            else:
                return (e1, tokens)
        elif (not e1 == None) and (tokens == []):
            return(e1, tokens)
        elif e1 == None:
            return (None, tokens)
    else:
        (e1, tokens) = leftFormula(tokens, False)
        if (not e1 == None) and (not tokens == []):
            if tokens[0] == "xor":
                (e2, tokens) = formula(tokens[1:])
                if not e2 == None:
                    return ({"Xor":[e1, e2]}, tokens)
                else:
                    return None
            #in top case, this is when it doesn't conform to the grammar.
            else:
                return None
        elif (not e1 == None) and (tokens == []):
            return(e1, tokens)
        else:
            return None

# added cases for extra credit
def leftFormula(tmp, top = True):
    seqs = [\
        ("True", ["true"]), \
        ("False", ["false"]), \
        ("Bool", ["bool", "(", term, ")"]), \
        ("Variable", [variable]), \
        ("Compare", ["(", term, "=", term, ")"]), \
        ("LessThan", ["(", term, "<", term, ")"]), \
        ("GreaterThan", ["(", term, ">", term, ")"]) \
        ]

    for (label, seq) in seqs:
        tokens = tmp[0:]
        ss = []
        es = []

        for x in seq:
            if type(x) == type(""): # Terminal.

                if tokens[0] == x:
                    # Does terminal match token?
                    tokens = tokens[1:]
                    ss = ss + [x]
                else:
                    break # Terminal did not match token.

            else: # Parsing function.

                # Call parsing function recursively
                r = x(tokens) 
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

        # Check that we got either a matched token
        # or a parse tree for each sequence entry.
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)
    return (None, tokens)

#1.c.
def term(tokens, top = True):
    #the check procedure of term() is similar to that of formula().
    if top == True:
        r = factor(tokens)
        if not r == None:
            (e1, tokens) = r
            if (not e1 == None) and (not len(tokens) == 0):
                if tokens[0] == "+":
                    (e2, tokens) = term(tokens[1:])
                    return({"Add":[e1, e2]}, tokens)
            return (e1, tokens)
        else:
            return None
    else:
        r = factor(tokens)
        if not r == None:
            (e1, tokens) = r
            if (not e1 == None) and (not len(tokens) == 0):
                if tokens[0] == "+":
                    (e2, tokens) = term(tokens[1:], False)
                    return ({"Add":[e1, e2]}, tokens)
                else:
                    return (e1, tokens)
            elif (not e1 == None) and (len(tokens) == 0):
                return (e1, tokens)
            elif e1 == None:
                return (None, tokens)
        else:
            return (None, tokens)
                
def factor(tokens):
    (e1, tokens) = leftFactor(tokens)
    if not len(tokens) == 0:
        if tokens[0] == "*":
            (e2, tokens) = factor(tokens[1:])
            if not e2 == None:
                return ({"Multiply":[e1, e2]}, tokens)
            else:
                return None
    if not e1 == None:
        return (e1, tokens)
    else:
        return None

def leftFactor(tokens):
    if tokens[0] == "int" and tokens[1] == "(":
        (e1, tokens) = formula(tokens[2:], False)
        if tokens[0] == ")":
            return ({"Int":[e1]}, tokens[1:])
    if tokens[0] == '(':
        (e1, tokens) = term(tokens[1:])
        if tokens[0] == ')':
            return ({'Parens':[e1]}, tokens[1:])

    if not variable(tokens) == None:
        (e1, tokens) = variable(tokens)
        return ({"Variable":[e1]}, tokens)

    if not number(tokens) == None:
        (e1, tokens) = number(tokens)
        return ({"Number":[e1]}, tokens)

    return (None, tokens)

#1.d.
def program(tokens, top = True):
    if tokens == []:
        return ("End", tokens)

    if tokens[0] == "print":
        #try both formula and term here
        (e0, tokens1) = formula(tokens[1:], False)
        (e1, tokens2) = term(tokens[1:], False)
        if len(tokens1) < len(tokens2):
            e1 = e0
            tokens = tokens1
        else:
            tokens = tokens2
        if not e1 == None:
            if tokens[0] == ";":
                (e2, tokens) = program(tokens[1:],False)
                if top == True and len(tokens) > 0:
                    return None
                else:
                    return ({"Print":[e1, e2]}, tokens)

    if tokens[0] == "assign":
        (e1, tokens) = variable(tokens[1:])
        if not e1 == None:
            if tokens[0] == "=":
                (e0, tokens1) = term(tokens[1:], False)
                (e2, tokens2) = formula(tokens[1:],False)
                if len(tokens1) < len(tokens2):
                    e2 = e0
                    tokens = tokens1
                else:
                    tokens = tokens2
                if not e2 == None:
                    if tokens[0] == ";":
                        (e3, tokens) = program(tokens[1:],False)
                        if top == True and e3 == None:
                            return None
                        else:
                            return ({"Assign":[{'Variable':[e1]}, e2, e3]}, tokens)

    if tokens[0] == 'if':
        (e1, tokens1) = formula(tokens[1:],False)
        (e0, tokens2) = term(tokens[1:], False)
        if len(tokens1) < len(tokens2):
            tokens = tokens1
        else:
            e1 = e0
            tokens = tokens2
        if not e1 == None:
            if tokens[0] == '{':
                (e2, tokens) = program(tokens[1:],False)
                if not e2 == None:
                    if tokens[0] == '}':
                        (e3, tokens) = program(tokens[1:], False)
                        if top == True and len(tokens)>0:
                            return None
                        else:
                            return ({'If':[e1,e2,e3]}, tokens)

    if tokens[0] == 'while':
        (e1, tokens1) = formula(tokens[1:],False)
        (e0, tokens0) = term(tokens[1:], False)
        if len(tokens1) < len(tokens0):
            tokens = tokens1
        else:
            e1 = e0
            tokens = tokens0
        if not e1 == None:
            if tokens[0] == '{':
                (e2, tokens) = program(tokens[1:],False)
                if not e2 == None:
                    if tokens[0] == '}':
                        (e3, tokens) = program(tokens[1:],False)
                        if top == True and e3 == None:
                            return None
                        else:
                            return ({'While':[e1,e2,e3]}, tokens)
    else:
        if top == True:
            return None
        else:
            return ("End", tokens)

def expression(tokens, top = True):
    r = formula(tokens, top)
    if not r == None:
        (e1, tokens1) = r

    r = term(tokens, top)
    if not r == None:
        (e2, tokens2) = r

    if top == True:
        if not e1 == None:
            return (e1, tokens1)
        else:
            return (e2, tokens2)
    elif top == False:
        if len(tokens1) < len(tokens2):
            return (e1, tokens1)
        else:
            return (e2, tokens2)
    
        
            
