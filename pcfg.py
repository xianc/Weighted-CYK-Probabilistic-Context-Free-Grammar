#Xian Chen (25781347)
#HW6: CS 453

import sys
from random import choice
from dicts import DefaultDict

def Dict(**args): 
    """Return a dictionary with argument names as the keys, 
    and argument values as the key values"""
    return args

# The grammar
# A line like:
#    NP = [['Det', 'N'], ['N'], ['N', 'PP'], 
# means
#    NP -> Det N
#    NP -> N
#    NP -> N PP
grammar = Dict(
        S = {('NPPL','NVPL'):.25, ('NPS','NVS'):.3, ('NPPL','VPPPL'):.2, ('NPS','VPPS'):.25},
        #noun phrase 
        NPPL = {('DetP', 'ADJNPL'):.4, ('DetP', 'NPL'):.6},
        NPS = {('DetS', 'ADJNS'):.3, ('DetS', 'NS'):.70},
        #adj plural and singular
        ADJNS = {('J', 'NS'):1},
        ADJNPL = {('J', 'NPL'):1},
        #verb singular/plural with noun phrase singular/plural
        NVS = {('VS','NPS'):1},
        NVPL = {('VPL','NPPL'):1},
        #singular/purple verb and noun with singular/plural prep phrase
        VPPPL = {('NVPL', 'PPPL'):.8, ('NVPL', 'PPS'):.2},
        VPPS = {('NVS', 'PPS'):.8, ('NVS', 'PPPL'):.1},
        #prep phrase
        PPS = {('P', 'NPS'):1},
        PPPL = {('P', 'NPPL'):1},
        #verbs that should be followed with "with"
        EDP = {('ED','P'):1},
        #training data
        DetS = {'the':.36, 'a':.65},
        DetP = {'the':1},
        P = {'with':1},
        J = {'red':.5, 'big':.5},
        NS = {'dog':float(1)/3, 'ball':float(1)/3, 'light':float(1/3)},
        NPL = {'dogs':.5, 'pickles':.5},
        VS = {'pickles':.25, 'sees':.25, 'liked':.25,'EDP':.25},
        VPL = {'see':float(1)/3, 'liked':float(1)/3, 'light':float(1)/3, 'EDP':1},
        ED = {'slept':1}
        )


#def generate(phrase):
#    "Generate a random sentence or phrase"
#    if isinstance(phrase, list): 
#        return mappend(generate, phrase)
#    elif phrase in grammar:
#        return generate(choice(grammar[phrase]))
#    else: return [phrase]
    
def generate_tree(phrase):
    """Generate a random sentence or phrase,
     with a complete parse tree."""
    if isinstance(phrase, list): 
        return map(generate_tree, phrase)
    elif phrase in grammar:
        return [phrase] + generate_tree(choice(grammar[phrase]))
    else: return [phrase]

def mappend(fn, list):
    "Append the results of calling fn on each element of list."
    return reduce(lambda x,y: x+y, map(fn, list))

def producers(constituent):
    #print constituent
    "Argument is a list containing the rhs of some rule; return all possible lhs's"
    results = []
    for (lhs,rhss) in grammar.items():
        for rhs in rhss:
            if rhs == constituent:
                results.append(lhs)

    return results

def printtable(table, wordlist):
    "Print the dynamic programming table.  The leftmost column is always empty."
    print "    ", wordlist
    for row in table:
	print row

def parse(sentence):
    "The CYK parser.  Return True if sentence is in the grammar; False otherwise"
    global grammar
    # Create the table; index j for rows, i for columns
    length = len(sentence)
    table = [None] * (length)
    table2 = DefaultDict(float)
    trace = {}

    for j in range(length):
	table[j] = [None] * (length+1)
	for i in range(length+1):
	    table[j][i] = []
    # Fill the diagonal of the table with the parts-of-speech of the words
    for k in range(1,length+1):
        results = producers(sentence[k-1])
        for item in results:
            list = (item, sentence[k-1])
            prob = grammar[item][sentence[k-1]]
            #print grammar[item][sentence[k-1]]
            table2[k-1,k, item] = prob
        table[k-1][k].extend(results)

    #Weighted CYK
    for width in range(2,length+1): 
        for start in range(0,length+1-width): 
            end = start + width 
            for mid in range (start, end): 
                max_score = 0
                args = None
                for x in table[start][mid]: 
                    for y in table[mid][end]:
                        #print x,y
                        results = producers((x,y))
                        for item in results:
                            prob1 = grammar[item][(x,y)]
                            prob2 = prob1 * table2[start, mid, x] * table2[mid, end, y]
                            checkme = start, end, item
                            if checkme in table2:
                                if prob2 > table2[start, end, item]:
                                    table2[start, end, item] = prob2
                            else:
                                table2[start, end, item] = prob2
                            args2 = x, y, mid
                            if args2 in trace:
                                if prob2 > table2[start, end, item]:
                                    args = x, y, mid
                                    trace[start, end, item] = args
                            else:
                                args = x, y, mid
                                trace[start, end, item] = args
                            trace[start, end, item] = args
                            if item not in table[start][end]:
                                table[start][end].append(item)


    # Print the table
    print "The Tags Table"
    printtable(table, sentence)

    print "\nProbability Table"
    print table2

    print "\nThe Parse Tree"
    if table2[0, length-1, 'S']:
        print get_tree(sentence, trace, 0, length, 'S')

def get_tree(x, trace, i, j, X):
    n = j - i
    if n == 1:
        return [X, x[i]]
    else:
        Y, Z, s = trace[i, j, X]
        return [X, get_tree(x, trace, i, s, Y),
                   get_tree(x, trace, s, j, Z)]
        

parse('the pickles light the dogs with the dog'.split())

