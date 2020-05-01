from graphviz import Digraph

class DFA_Acceptor:

    def __init__(self, nume):

        f = open('%s' % nume, 'r')
        self.alphabet = f.readline().split()
        self.states = f.readline().split()
        self.initial_state = f.readline().strip()
        self.actual_state = self.initial_state
        self.final_states = f.readline().split()
        self.data = []
        self.solution = []

        for transition in [x for x in f.readline().split(', ')]:
            self.data.append((transition[0], transition[2], transition[4]))

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
                    transition = [x for x in self.data if x[0] == self.actual_state and x[1] == character]
                    if transition == []:
                        ok = 0
                        break
                    else:
                        self.actual_state = transition[0][2]
                        self.solution.append(*transition)

                if self.actual_state in self.final_states and ok == 1:
                    print("%s ∈ DFA." % self.word)
                else:
                    print("%s ∉ DFA, as the word ends in a non-final state." % self.word)
                    self.solution = []

    def draw(self, graph_color, solution_color):
        graph = Digraph('G', filename = 'Deterministic Finite Automata Acceptor', format = 'png')
        graph.attr('node', shape = 'doublecircle')

        for current_node in self.final_states:
            graph.node('%s' % current_node)

        graph.attr('node', shape = 'circle')
        graph.node('%s' % self.initial_state)

        graph.attr('node', shape = 'none')
        graph.edge('', '%s' % self.initial_state, label = 'Start')

        graph.attr('node', shape = 'circle')

        for transition in self.data:
            if transition in self.solution:
                graph.attr('edge', color = solution_color)
                graph.edge('%s' % transition[0], '%s' % transition[2], label = '%s' % transition[1])
                graph.attr('edge', color = graph_color)
            else:
                graph.edge('%s' % transition[0], '%s' % transition[2], label = '%s' % transition[1])
        graph.view()

def main():
    a = DFA_Acceptor('data.in')
    a.check_acceptance()
    a.draw('red', 'blue')


if __name__ == "__main__":
    main()
