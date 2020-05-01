from graphviz import Digraph

class DeterministicFiniteAutomata:

    def __init__(self, nume):

        f = open('%s' % nume, 'r')
        self.alphabet = f.readline().split()
        self.states = f.readline().split()
        self.initial_state = f.readline().strip()
        self.actual_state = self.initial_state
        self.states_finale = f.readline().split()
        aux = [x for x in f.readline().split(', ')]
        self.DeterministicFiniteAutomata = []
        self.solution = []

        for elem in aux:
            self.DeterministicFiniteAutomata.append((elem[0], elem[2], elem[4]))
        self.word = f.readline()

    def check_acceptance(self):

        ok = 1
        valid_alphabet = 1

        for letter in self.word:
            if letter not in self.states:
                print("The word contains a letter that is not part of the alphabet.")
                valid_alphabet = 0
                break

        if valid_alphabet:
            if self.word == 'lambda' or self.word == '':
                print("λ ∈ DFA.")
            else:
                for character in self.word:
                    transition = [x for x in self.DeterministicFiniteAutomata if x[0] == self.actual_state and x[1] == character]
                    if transition == []:
                        ok = 0
                        break
                    else:
                        self.actual_state = transition[0][2]
                        self.solution.append(*transition)

                if self.actual_state in self.states_finale and ok == 1:
                    print("%s ∈ DFA." % self.word)
                else:
                    print("%s ∉ DFA, as the word ends in a non-final state." % self.word)
                    self.solution = []

    def draw(self, culoare_graf, culoare_sol):
        g = Digraph('G', filename = 'DeterministicFiniteAutomata', format = 'png')
        g.attr('node', shape = 'doublecircle')

        for current_node in self.states_finale:
            g.node('%s' % current_node)

        g.attr('node', shape = 'circle')
        g.node('%s' % self.initial_state)

        g.attr('node', shape = 'none')
        g.edge('', '%s' % self.initial_state, label = 'Start')

        g.attr('node', shape = 'circle')

        for transition in self.DeterministicFiniteAutomata:
            if transition in self.solution:
                g.attr('edge', color = culoare_sol)
                g.edge('%s' % elem[0], '%s' % elem[2], label = '%s' % elem[1])
                g.attr('edge', color = culoare_graf)
            else:
                g.edge('%s' % elem[0], '%s' % elem[2], label = '%s' % elem[1])
        g.view()


if __name__ == "__main__":
    a = DeterministicFiniteAutomata('data.in')
    a.check_acceptance()
    a.draw('red', 'blue')
