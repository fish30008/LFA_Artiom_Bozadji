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

    # def generateString(self):
    #     current = self.start
    #     result = []
    #     while current in self.Vn:
    #         production = random.choice(self.P[current]) ## without random production = self.P[current_symbol][0]
    #         if result[i].__contains__(self.Vn):
    #             current = production[-1]
    #             continue
    #         result.append(production)
    #         current = production[-1]
    #     return ''.join(result)

    def generateString(self):
        current = self.start
        # result = []

        while any(symbol in self.Vn for symbol in current):
            new_string = ""
            for symbol in current:
                if symbol in self.Vn:
                    new_string += random.choice(self.P[symbol])
                else:
                    new_string += symbol
            current = new_string  # Update current string

        return current


    def toFiniteAutomaton(self):
            return FiniteAutomaton(self.P, self.start)


class FiniteAutomaton:
    def __init__(self, transitions, start):
        self.transitions = transitions
        self.start = start

    def stringBelongToLanguage(self, input_string):
        current = self.start
        for char in input_string:
            found_transition = False
            for transition in self.transitions.get(current, []):
                if transition[0] == char:
                    current = transition[1]
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
print(str(fa.start) + '<- start----transitions ->' + str(fa.transitions))
print("\nFinite Automaton string checks:")

text = 'abc'
print(fa.stringBelongToLanguage(text))


