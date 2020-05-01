This program verifies if a given DFA accepts a word.\
It uses the module "graphviz" to draw the graph associated to the DFA as a PNG file.\
The input must match this format:\
  The first and second lines have the states, respectively the alphabet, with spaces in-between.\
  The third and fourth lines contain the initial state, respectively the final states, with spaces in-between.\
  The 5th line has the transitions of the DFA, separated by ", ", in the following pattern: state1 word_from_alphabet state2.\
  The 6th line contains the word.\
