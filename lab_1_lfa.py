'''public class Grammar
{
    public Grammar(some params...)
    public String generateString()
    public FiniteAutomaton toFiniteAutomaton()


public class FiniteAutomaton
{
    public FiniteAutomaton(constructor params...)


    public boolean stringBelongToLanguage(final String inputString)

}'''


'''
Variant 3:
VN={S, D, R}, 
VT={a, b, c, d, f},
P={ 
    S → aS
    S → bD
    S → fR
    D → cD
    D → dR
    R → bR
    R → f
    D → d
}'''
import random
class Grammar:
    def __init__(self):
        self.Vn = ['S', 'D', 'R']
        self.Vt = ['a', 'b', 'c', 'd', 'f']  # Terminal symbols
        self.P = {
            'S': ['aS', 'bD', 'fR'],
            'D': ['cD', 'dR', 'd'],
            'R': ['bR', 'f']}
        self.start = 'S'

    def generateString(self):
        current = self.start
        result = []
        while current in self.Vn:
            production = random.choice(self.P[current])
            result.append(production)
            current = production[-1]
        return ''.join(result)



    def toFiniteAutomaton(self):
            return FiniteAutomaton(self.P, self.start)


class FiniteAutomaton:
    def __init__(self, transitions, start_state):
        self.transitions = transitions
        self.start_state = start_state

    def stringBelongToLanguage(self, input_string):
        current_state = self.start_state
        for char in input_string:
            found_transition = False
            for transition in self.transitions.get(current_state, []):
                if transition[0] == char:
                    current_state = transition[1]
                    found_transition = True
                    break
            if not found_transition:
                return False
        return True


grammar = Grammar()
print("Generated strings:")
for _ in range(5):
    print(grammar.generateString())

fa = grammar.toFiniteAutomaton()
print("\nFinite Automaton string checks:")

for text in grammar.P.values():
    print(fa.stringBelongToLanguage(text))


