#####################################################################
#
# CAS CS 320, Spring 2015
# Midterm (skeleton code)
# validate.py
# Linshan Jiang (linshan@bu.edu)
#
#  ****************************************************************
#  *************** Modify this file for Problem #4. ***************
#  ****************************************************************
#

exec(open('interpret.py').read())
exec(open('compile.py').read())

def expressions(n):
    if n <= 0:
        []
    elif n == 1:
        return ["True", "False"] # Add base case(s) for Problem #5.
    else:
        es = expressions(n-1)
        esN = []
        esN += [{"Number": [2]}]
        esN += [{"Variable": ["a"]}]
        esN += [{"Array": [{"Variable": ["a"]}, e]} for e in es]
        return es + esN

def programs(n):
    if n <= 0:
        []
    elif n == 1:
        return ['End']
    else:
        ps = programs(n-1)
        es = expressions(n-1)
        psN = []
        psN += [{'Assign':[{'Variable':['a']}, e, e, e, p]} for p in ps for e in es]
        psN += [{"Print": [e, p]} for p in ps for e in es]
        psN += [{"For": [{"Variable": ["x"]}, p1, p2]} for p1 in ps for p2 in ps]
        return ps + psN

# We always add a default assignment to the program in case
# there are variables in the parse tree returned from programs().

def defaultAssigns(p):
    return \
      {'Assign':[\
        {'Variable':['a']}, {'Number':[2]}, {'Number':[2]}, {'Number':[2]}, p\
      ]}

# Compute the formula that defines correct behavior for the
# compiler for all program parse trees of depth at most 4.
# Any outputs indicate that the behavior of the compiled
# program does not match the behavior of the interpreted
# program.

def transResult(x):
    if not x == []:
        new = []
        # there are two types of x, simple means it contains only integers,
        # for example, x = [2,2,2] and it should be converted to [2]
        # the complex type of x occurs when x inclutes either a list or "True", "False"
        typeX = "simple"
        for i in range(len(x)):
            if type(x[i]) == list or x[i] == "True" or x[i] == "False":
                typeX = "complex"
                break
        # this will convert the resulting array into the first entry of the array.
        if typeX == "simple":
            new = [x[0]]
        else:
            for i in range(len(x)):
                #x[i] is either a list or an integer.
                children = x[i]
                if not type(children) == list:
                    # "True" is converted to the coresponding interger 1
                    if children == "True":
                        new += [1]
                    # "False" is converted to the coresponding interger 0
                    if children == "False":
                        new += [0]
                    elif type(children) == int:
                        new += [children]
                if type(children) == list:
                    new += [children[0]]
        x = new

    return x

for p in [defaultAssigns(p) for p in programs(3)]:
    try:
        x = execute({}, p)[1]
        # transResult is a conversion function that converts the
        # abstract syntax trees into the corresponding
        # integer values that can appear in machine memory addresses.
        x = transResult(x)
        if simulate(compileProgram({}, unrollLoops(p))[1]) != x:
            print('\nIncorrect behavior on: ' + str(p))
    except:
        print('\nError on: ' + str(p))

#eof
