#Yida Xu  U39436573 xyds152@bu.edu  parse.py

from math import log, floor
import re


#1.a.
def variable(tokens):
    if tokens[0] != 'true' and tokens[0] != 'false':
        if re.match("^[a-z]$", tokens[0][0]):
            return (tokens[0], tokens[1:])

def number(tokens):
    if re.match(r"^([-]?[0-9]*[1-9]*)$", tokens[0]):
        return (int(tokens[0]), tokens[1:])


#1.b.
def formula(tokens):
    (e1, tokens) = leftForm(tokens)
    if not tokens == []:
        if tokens[0] == 'xor':
            (e2, tokens) = formula(tokens[1:])
            return ({'Xor':[e1, e2]}, tokens)
    return (e1, tokens)

    
def leftForm(tokens):
    if tokens[0] == 'true':
        return ('True', tokens[1:])
    
    if tokens[0] == 'false':
        return ('False', tokens[1:])
    
    if tokens[0] == '(':
        (e1, tokens) = formula(tokens[1:])
        if tokens[0] == ')':
            return ({'Parens':[e1]}, tokens[1:])
        
    if tokens[0] == 'not' and tokens[1] == '(':
        (e1, tokens) = formula(tokens[2:])
        if tokens[0] == ')':
            return ({'Not':[e1]}, tokens[1:])
        
    if variable(tokens) != None:
        (e1, tokens) = variable(tokens)
        return ({'Variable':[e1]}, tokens)

    else:
        return (None, tokens)


#1.c.
def term(tokens):
    (e1, tokens) = factor(tokens)
    if not tokens == []:
        if tokens[0] == '+':
            (e2, tokens) = term(tokens[1:])
            return ({'Plus': [e1, e2]}, tokens)
    return (e1, tokens)

    
def factor(tokens):
    (e1, tokens) = leftFactor(tokens)
    if not tokens == []:
        if tokens[0] == '*':
            (e2, tokens) = factor(tokens[1:])
            return ({'Mult': [e1, e2]}, tokens)
    return (e1, tokens)

    
def leftFactor(tokens):
    if tokens[0] == 'log' and tokens[1] == '(':
        (e1, tokens) = term(tokens[2:])
        if tokens[0] == ')':
            return ({'Log':[e1]}, tokens[1:])

    if tokens[0] == '(':
        (e1, tokens) = term(tokens[1:])
        if tokens[0] == ')':
            return ({'Parens':[e1]}, tokens[1:])

    if variable(tokens) != None:
        (e1, tokens) = variable(tokens)
        return ({'Variable':[e1]}, tokens)

    if number(tokens) != None:
        (e1, tokens) = number(tokens)
        return ({'Number':[e1]}, tokens)

    else:
        return (None, tokens)

#1.d.
def program(tokens):
    if tokens == []:
        return ('End', tokens)
    if tokens[0] != 'print' and tokens[0] != 'assign' and tokens[0] != 'while' and tokens[0] != 'if':
        return ('End', tokens)
    
    if tokens[0] == 'print':
        (e1, tokens) = expression(tokens[1:])
        if tokens[0] == ';':
            (e2, tokens) = program(tokens[1:])
            return ({'Print':[e1,e2]}, tokens)

    if tokens[0] == 'assign':
        (e1, tokens) = variable(tokens[1:])
        if tokens[0] == ':=':
            (e2, tokens) = expression(tokens[1:])
            if tokens[0] == ';':
                (e3, tokens) = program(tokens[1:])
                return ({'Assign':[{'Variable':[e1]}, e2 ,e3]}, tokens)

    if tokens[0] == 'if':
        (e1, tokens) = expression(tokens[1:])
        if tokens[0] == '{':
            (e2, tokens) = program(tokens[1:])
            if tokens[0] == '}':
                (e3, tokens) = program(tokens[1:])
                return ({'If':[e1,e2,e3]}, tokens)

    if tokens[0] == 'while':
        (e1, tokens) = expression(tokens[1:])
        if tokens[0] == '{':
            (e2, tokens) = program(tokens[1:])
            if tokens[0] == '}':
                (e3, tokens) = program(tokens[1:])
                return ({'While':[e1,e2,e3]}, tokens)

def expression(tmp):
    (e1, tokens) = formula(tmp)
    if (tokens[0] == '{' or tokens[0] == ';') and not e1 == None:
        return (e1, tokens)
    (e1, tokens) = term(tmp)
    if (tokens[0] == '{' or tokens[0] == ';') and not e1 == None:
        return (e1, tokens)

    (e1, tokens) = formula(tmp)
    if tokens[0] == '==':
        (e2, tokens) = formula(tokens[1:])
        if (tokens[0] == '{' or tokens[0] == ';') and not e2 == None:
            return ({'Equal':[e1,e2]}, tokens)

    (e1, tokens) = term(tmp)
    if tokens[0] == '==':
        (e2, tokens) = term(tokens[1:])
        if (tokens[0] == '{' or tokens[0] == ';') and not e2 == None:
            return ({'Equal':[e1,e2]}, tokens)
    elif tokens[0] == '<':
        (e2, tokens) = term(tokens[1:])
        if (tokens[0] == '{' or tokens[0] == ';') and not e2 == None:
            return ({'LessThan': [e1,e2]}, tokens)
