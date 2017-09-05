#hw1
#Linshan Jiang (linshan@bu.edu)

#1.a.
import re
def tokenize(terminals, syntax):
    s = "(\s+"
    for i in terminals:
        if i == "*" or i == "+" or i == "|" or i == "(" or i == ")" or i == ";" \
           or i == "\\" or i == "." or i == "^" or i == "$":
            s += ("|" + "\\" + i)
        else:
            s += ("|" + i)
    s += ")"
            
    # Use a regular expression to split the string into
    # tokens or sequences of zero or more spaces.
    tokens = [t for t in re.split(s, syntax)]

    # Throw out the spaces and return the result.
    return [t for t in tokens if not t.isspace() and not t == ""]

#1.b.
def transformation(tokens):
    if tokens[0] == "projection" and tokens[1] == ";":
        (e1, tokens) = transformation(tokens[2:])
        return ({"Projection": [e1]}, tokens)
    if tokens[0] == "reflection" and tokens[1] == ";":
        (e1, tokens) = transformation(tokens[2:])
        return ({"Reflection": [e1]}, tokens)
    if tokens[0] == "left" and tokens[1] == "rotation" and tokens[2] == ";":
        (e1, tokens) = transformation(tokens[3:])
        return ({"LeftRotation": [e1]}, tokens)
    if tokens[0] == "right" and tokens[1] == "rotation" and tokens[2] == ";":
        (e1, tokens) = transformation(tokens[3:])
        return ({"RightRotation": [e1]}, tokens)
    if tokens[0] == "finish":
        return ("Finish", tokens[2:])

#2.
def number(tokens):
    #changed to match both positive or negative integers
    if re.match(r"^((-)?[1-9][0-9]*)$", tokens[0]):
        return ({"Number": [int(tokens[0])]}, tokens[1:])

#2.a.
def variable(tokens):
    if re.match(r"^([a-z]*)$", tokens[0]):
        return ({"Variable": [tokens[0]]}, tokens[1:])

#2.b. / #3.
def term(tmp, top = True):

    
#the reason why I use redundant algorithum for term() and program()
#is that these two funtions involve calling variable() and number().
#in order not to double print "Variable" and "Number", I need to make
#special changes for these two cases.

    
    #add
    tokens = tmp[0:]
    if tokens[0] == "add" and tokens[1] == "(":
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ",":
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ")":
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return({"Add": [e1,e2]}, tokens)
    #subtract
    tokens = tmp[0:]
    if tokens[0] == "subtract" and tokens[1] == "(":
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ",":
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ")":
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return({"Subtract": [e1,e2]}, tokens)
    #abs
    tokens = tmp[0:]
    if tokens[0] == "abs" and tokens[1] == "(":
        tokens = tokens[2:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ")":
                tokens = tokens[1:]
                if not top or len(tokens) == 0:
                    return({"Abs": [e1]}, tokens)
    #variable
    tokens = tmp[0:]
    if tokens[0] == "@":
        tokens = tokens[1:]
        r = variable(tokens)
        if not r is None:
            (e1, tokens) = r
            if not top or len(tokens) == 0:
                return(e1, tokens)
    #nuber
    tokens = tmp[0:]
    if tokens[0] == "#":
        tokens = tokens[1:]
        r = number(tokens)
        if not r is None:
            (e1, tokens) = r
            if not top or len(tokens) == 0:
                return(e1, tokens)


    #add
    tokens = tmp[0:]
    if tokens[0] == "(":
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == "+":
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ")":
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return({"Add": [e1,e2]}, tokens)

    #subtract
    tokens = tmp[0:]
    if tokens[0] == "(":
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == "-":
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ")":
                        tokens = tokens[1:]
                        if not top or len(tokens) == 0:
                            return({"Subtract": [e1,e2]}, tokens)

    #abs
    tokens = tmp[0:]
    if tokens[0] == "|":
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == "|":
                tokens = tokens[1:]
                if not top or len(tokens) == 0:
                    return({"Abs": [e1]}, tokens)
#2.c. / #3.
def formula(tmp, top = True):
    seqs = [\
        ("True", ["true"]), \
        ("False", ["false"]), \
        ("Not", ["not", "(", formula, ")"]), \
        ("And", ["and", "(", formula, ",", formula, ")"]), \
        ("Or", ["or", "(", formula, ",", formula, ")"]), \
        ("Compare", ["compare", "(", term, ",", term, ")"]), \
        ("LessThan", ["less", "than", "(", term, ",", term, ")"]), \
        ("GreaterThan", ["greater", "than", "(", term, ",", term, ")"]), \
        ("And", ["(", formula, "&&", formula, ")"]), \
        ("Or", ["(", formula, "|","|", formula, ")"]), \
        ("Compare", ["(", term, "=", term, ")"]), \
        ("LessThan", ["(", term, "<", term, ")"]), \
        ("GreaterThan", ["(", term, ">", term, ")"]) \
        ]

    #below is capied from lecture notes.
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
                r = x(tokens, False) 
                if not r is None:
                    (e, tokens) = r
                    es = es + [e]

        # Check that we got either a matched token
        # or a parse tree for each sequence entry.
        if len(ss) + len(es) == len(seq):
            if not top or len(tokens) == 0:
                return ({label:es} if len(es) > 0 else label, tokens)

#2.d.
def program(tmp, top = True):
    #first print case
    tokens = tmp[0:]
    if tokens[0] == "print":
        tokens = tokens[1:]
        r = formula(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ";":
                tokens = tokens[1:]
                r = program(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if not top or len(tokens) == 0:
                        return ({"Print": [e1,e2]}, tokens)
    #second print case
    tokens = tmp[0:]
    if tokens[0] == "print":
        tokens = tokens[1:]
        r = term(tokens, False)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == ";":
                tokens = tokens[1:]
                r = program(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if not top or len(tokens) == 0:
                        return ({"Print": [e1,e2]}, tokens)
    #assign
    tokens = tmp[0:]
    if tokens[0] == "assign" and tokens[1] == "@":
        tokens = tokens[2:]
        r = variable(tokens)
        if not r is None:
            (e1, tokens) = r
            if tokens[0] == "=":
                tokens = tokens[1:]
                r = term(tokens, False)
                if not r is None:
                    (e2, tokens) = r
                    if tokens[0] == ";":
                        tokens = tokens[1:]
                        r = program(tokens, False)
                        if not r is None:
                            (e3, tokens) = r
                            if not top or len(tokens) == 0:
                                return ({"Assign": [e1,e2,e3]}, tokens)
    #end
    tokens = tmp[0:]
    if tokens[0] == "end" and tokens[1] == ";":
        tokens = tokens[2:]
        if not top or len(tokens) == 0:
            return ("End", tokens)

#2.e.
def complete(string):
    terminals = ["print", ";", "assign", "@", "=", ";", "end", "true", "false", \
                 "not", "(", ")", "and", ",", "or", "compare", "less", "than", "greater", \
                 "than", "&&", "<", ">", "add", "subtract", "abs", "#", "+", "-", "|"]
    tokens = tokenize(terminals, string)
    #check if the tokens match program case
    if tokens[0] == "print" or tokens[0] == "assign" or tokens[0] == "end":
        r = program(tokens)
        if not r is None:
            (e1, tokens) = r
            return e1
    #check if the tokens match formula case
    elif tokens[0] == "true" or tokens[0] == "false" or tokens[0] == "not" \
         or tokens[0] == "and" or tokens[0] == "or" or tokens[0] == "compare" \
         or tokens[0] == "less" or tokens[0] == "greater":
        r = formula(tokens)
        if not r is none:
            (e2, tokens) = r
            return e2
    #check if the tokens match term case
    elif tokens[0] == "add" or tokens[0] == "subtract" or tokens[0] == "abs" \
         or tokens[0] == "@" or tokens[0] == "#" or tokens[0] == "|":
        r = term(tokens)
        if not r is None:
            (e3, tokens) = r
            return e3
    #but, there is a special case if tokens begin with "(", as it both
    #satisfies formula and term case. So try both... Not efficient though...
    elif tokens[0] == "(":
        r = formula(tokens)
        if r is None:
            r = term(tokens)
            if not r is None:
                (e4, tokens) = r
                return e4
        else:
            (e5, tokens) = r
            return e5


