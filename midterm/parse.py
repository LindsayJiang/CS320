#####################################################################
#
# CAS CS 320, Spring 2015
# Midterm (skeleton code)
# parse.py
# Linshan Jiang(linshan@bu.edu)
#
#  ****************************************************************
#  *************** Modify this file for Problem #1. ***************
#  ****************************************************************
#

import re

def number(tokens, top = True):
    if re.compile(r"(-(0|[1-9][0-9]*)|(0|[1-9][0-9]*))").match(tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

def variable(tokens, top = True):
    if re.compile(r"[a-z][A-Za-z0-9]*").match(tokens[0]) and tokens[0] not in ['true', 'false']:
        return ({"Variable": [tokens[0]]}, tokens[1:])

def expression(tokens):
    # Complete for Problem #1.
    (e1, tokens) = leftExpression(tokens)
    if not tokens == []:
        if tokens[0] == "+":
            (e2, tokens) = expression(tokens[1:])
            return ({"Plus":[e1,e2]}, tokens)
    return (e1, tokens)


def leftExpression(tokens):
    if tokens[0] == "true":
        return ("True", tokens[1:])

    if tokens[0] == "false":
        return ("False", tokens[1:])

    if tokens[0] == "@":
        (e1, tokens) = variable(tokens[1:])
        if tokens[0] == "[":
            (e2, tokens) = expression(tokens[1:])
            if tokens[0] == "]":
                return ({"Array":[e1,e2]}, tokens[1:])

    if not (variable(tokens) == None):
        (e1, tokens) = variable(tokens)
        return (e1, tokens)

    if not (number(tokens) == None):
        (e1, tokens) = number(tokens)
        return (e1, tokens)

    else:
        return (None, tokens)

def program(tokens):
    # Complete for Problem #1.
    if tokens == []:
        return ("End", tokens)

    if tokens[0] == "print":
        (e1, tokens) = expression(tokens[1:])
        if tokens[0] == ";":
            (e2, tokens) = program(tokens[1:])
            return ({"Print":[e1,e2]}, tokens)

    if tokens[0] == "for":
        (e1, tokens) = variable(tokens[1:])
        if tokens[0] == "{":
            (e2, tokens) = program(tokens[1:])
            if tokens[0] == "}":
                (e3, tokens) = program(tokens[1:])
                return ({"For":[e1,e2,e3]}, tokens)
    else:
        if not (variable(tokens[0]) == None):
            (e1, tokens) = variable(tokens)
            if tokens[0] == "=" and tokens[1] == "[":
                (e2, tokens) = expression(tokens[2:])
                if tokens[0] == ",":
                    (e3, tokens) = expression(tokens[1:])
                    if tokens[0] == ",":
                        (e4, tokens) = expression(tokens[1:])
                        if tokens[0] == "]" and tokens[1] == ";":
                            (e5, tokens) = program(tokens[2:])
                            return ({"Assign":[e1,e2,e3,e4,e5]}, tokens)
        else:
            return ("End", tokens)


def tokenizeAndParse(s):
    tokens = re.split(r"(\s+|=|print|@|\+|for|{|}|;|\[|\]|,)", s)
    tokens = [t for t in tokens if not t.isspace() and not t == ""]
    # Complete for Problem #1.
    (tree, left) = program(tokens)
    return tree


#eof
