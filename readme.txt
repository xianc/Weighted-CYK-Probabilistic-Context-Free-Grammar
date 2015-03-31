Xian Chen


Implementation of Weighted CYK/Probabilistic Context Free Grammar:

Alterations/Additions:

1. Dictionary
To implement weighted CYK, I changed the dictionary, called grammar, from the previous homework assignment to a dictionary of dictionaries. The new grammar takes in tags as keys and each key contain dictionary items of tuples and their probability or a list of words and their corresponding probabilities

2. Parse Method
table2: “table2” is the table of probabilities that corresponds to “table”, a table of tags
trace: “trace” is declared as an empty list. It will be updated to contain the path of the sentence of the highest probability

The Parse method takes in a sentence and fills “table” and “table2.” While the method fills the diagonals of “table”, it fills in “table2” with the corresponding probabilities. 

On lines 113-143 in the code, weighted CYK is implemented. As we loop through the length of the sentence, we keep track of the path in which the algorithm takes to produce a sentence. Along the way, we calculate the probabilities of the path by multiplying the probability of being in the current state by the probability of being in the previous states. Table2 is then checked to see if the tag tuple is already exist. If it does, we check the probability of the tag tuple in the table. If the probability that exist in the table is less than the current probability of the tag tuple, then the entry in the table is replaced with the current one. The “trace” list is also updated with the higher probability entry. If the tag tuple is not in the table, it is simply added to the table and the “trace” list.  This functionality can be observed from line 113 to line 143 in the code. 

We then check “table2” to see if a sentence ‘S’ exist. If it does, the parse tree of the most probable sentence is printed. This is done by calling the get_tree method that was created (lines 157-164). 

Output: parse('the dog sees the ball'.split())
The Tags Table
     ['the', 'dog', 'sees', 'the', 'ball']
[[], ['DetP', 'DetS'], ['NPS'], [], [], ['S']]
[[], [], ['NS'], [], [], []]
[[], [], [], ['VS'], [], ['NVS']]
[[], [], [], [], ['DetP', 'DetS'], ['NPS']]
[[], [], [], [], [], ['NS']]

Probability Table
{(0, 1, 'DetS'): 0.36, (0, 2, 'NPS'): 0.08399999999999999, (3, 4, 'DetS'): 0.36, (1, 2, 'NS'): 0.3333333333333333, (4, 5, 'NS'): 0.3333333333333333, (0, 5, 'S'): 0.0005291999999999999, (3, 5, 'NPS'): 0.08399999999999999, (0, 1, 'DetP'): 1, (2, 5, 'NVS'): 0.020999999999999998, (2, 3, 'VS'): 0.25, (3, 4, 'DetP'): 1}

The Parse Tree
['S', ['NPS', ['DetS', 'the'], ['NS', 'dog']], ['NVS', ['VS', 'sees'], ['NPS', ['DetS', 'the'], ['NS', 'ball']]]]

As we can observe from the above parse tree, the program produced a correct parse tree for the sentence. NPS = Noun phrase singular; NVS = Verb Phrase Singular. NPS contains a determinator and a noun and NVS contains a verb, and a NPS, noun phrase singular. NPS is composed of a determinator and a noun phrase. 

Now lets observe the following sentence: “a big dog pickles a dog”
To the average user, the sentence is strange. Also pickles can either be a noun phrase plural (NPL), or a verb phrase singular (VS). When running the sentence on the program, we receive the following parse tree:

The Parse Tree
['S', ['NPS', ['DetS', 'a'], ['ADJNS', ['J', 'big'], ['NS', 'dog']]], ['NVS', ['VS', 'pickles'], ['NPS', ['DetS', 'a'], ['NS', 'dog']]]]

Not only does the program correctly select “pickles” to be a verb, it also correctly determined that the unusual sentence is in fact, a sentence. 



Multiple Possible Parse Trees/Ambiguous Parts-of-speech:
Now observing an even stranger sentence: “the big pickles liked the pickles with the red pickles”, the program outputs:

The Parse Tree
['S', ['NPPL', ['DetP', 'the'], ['ADJNPL', ['J', 'big'], ['NPL', 'pickles']]], ['VPPPL', ['NVPL', ['VPL', 'liked'], ['NPPL', ['DetP', 'the'], ['NPL', 'pickles']]], ['PPPL', ['P', 'with'], ['NPPL', ['DetP', 'the'], ['ADJNPL', ['J', 'red'], ['NPL', 'pickles']]]]]]

Again, a valid parse tree is produced. Notice that the sentence can be read as:
1. (NP(the big pickles)VP (like NP(the pickles with the red pickles))) or
2. (NP(the big pickles) VP(VP(like the pickles) PP(with (the red pickles))))  

The first sentence says:  the pickles with the red pickles were liked by the big pickles
The second sentence says: The pickles were liked by the big pickles and the red pickles

Notice that the program chose the highest probable parse as parse2 where the Verb Phrase is broken down to a verb phrase and a prepositional phrase. The program could’ve chosen the parse where the Verb Phrase is broken down to a verb phrase and a noun phrase. If we observe the dictionary of dictionaries (“grammar”) and calculate out the probabilities, we can see that the probability for a Verb Phrase containing a verb phrase and a prepositional phrase is set to be higher than a Verb Phrase containing a verb phrase and a Noun Phrase. 


In a similar case, the sentence “the dogs liked the red pickles with a ball” has multiple parse trees. 

(the dog) (liked (the red pickles with a ball))
(the dog) (liked (the red pickles) (with a ball))

The first sentence says: the red pickles with the ball are liked by the dog
The second sentence says: the red pickles are liked by the dog if the red pickles are with a ball

['S', ['NPPL', ['DetP', 'the'], ['NPL', 'dogs']], ['VPPPL', ['NVPL', ['VPL', 'liked'], ['NPPL', ['DetP', 'the'], ['ADJNPL', ['J', 'red'], ['NPL', 'pickles']]]], ['PPS', ['P', 'with'], ['NPS', ['DetS', 'a'], ['NS', 'ball']]]]]

Again, since the probability for a verb phrase containing a noun phrase and a prepositional phrase is set to be higher than a verb phrase containing a verb phrase and a noun phrase, the program chose the 2nd parse tree. 


Again, another example: “the pickles light the dogs with the dog”
(the pickles) (light (the dogs with the dog))
(the pickles)((light the dogs)(with the dog))

The first sentence says: the dogs with the dog were lit by the pickles
The second sentence says: the dogs were lit by the pickles and the dog

The Parse Tree
['S', ['NPPL', ['DetP', 'the'], ['NPL', 'pickles']], ['VPPPL', ['NVPL', ['VPL', 'light'], ['NPPL', ['DetP', 'the'], ['NPL', 'dogs']]], ['PPS', ['P', 'with'], ['NPS', ['DetS', 'the'], ['NS', 'dog']]]]]



