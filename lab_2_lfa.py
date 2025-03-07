from collections import deque

class Grammar:
    def __init__(self):
        self.Vn = []
        self.Vt = []
        self.P = {}
        self.start = ''

    def display(self):
        print("Regular Grammar:")
        print(f"Non-terminals (Vn): {self.Vn}")
        print(f"Terminals (Vt): {self.Vt}")
        print(f"Start symbol: {self.start}")
        print("Productions (P):")
        for nt, prods in self.P.items():
            print(f"  {nt} -> {' | '.join(prods) if prods else 'ε'}")
#
class NDFA:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def to_regular_grammar(self):
        grammar = Grammar()
        grammar.Vn = self.states
        grammar.Vt = self.alphabet
        grammar.start = self.initial_state

        for state in self.states:
            productions = []
            for symbol in self.alphabet:
                next_states = self.transitions[state][symbol]
                for next_state in next_states:
                    productions.append(f"{symbol}{next_state}")
            if state in self.final_states:
                productions.append('ε')
            grammar.P[state] = productions

        return grammar

    def is_dfa(self):
        for state in self.states:
            for symbol in self.alphabet:
                next_states = self.transitions[state][symbol]
                if len(next_states) != 1:  # Must have exactly one next state
                    return False
        return True

    def to_dfa(self):
        dfa_states = []
        dfa_transitions = {}
        dfa_initial = frozenset([self.initial_state])
        dfa_final = []
        queue = deque([dfa_initial])
        visited = set()

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)
            dfa_states.append(current)

            # Check if current state is final
            if any(state in self.final_states for state in current):
                dfa_final.append(current)

            # Compute transitions
            dfa_transitions[current] = {}
            for symbol in self.alphabet:
                next_set = set()
                for state in current:
                    next_set.update(self.transitions[state].get(symbol, set()))
                next_frozenset = frozenset(next_set)
                dfa_transitions[current][symbol] = next_frozenset
                if next_frozenset not in visited:
                    queue.append(next_frozenset)

        return DFA(dfa_states, self.alphabet, dfa_transitions, dfa_initial, dfa_final)

# Define the DFA class to store the result of conversion
class DFA:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def display(self):
        print("\nDFA Description:")
        print("States:", [','.join(sorted(s)) if s else '∅' for s in self.states])
        print("Alphabet:", self.alphabet)
        print("Initial State:", ','.join(sorted(self.initial_state)))
        print("Final States:", [','.join(sorted(s)) if s else '∅' for s in self.final_states])
        print("Transitions:")
        for state in self.states:
            state_str = ','.join(sorted(state)) if state else '∅'
            for symbol in self.alphabet:
                next_state = self.transitions[state][symbol]
                next_str = ','.join(sorted(next_state)) if next_state else '∅'
                print(f"  δ({state_str}, {symbol}) = {next_str}")


if __name__ == "__main__":
    # Variant 3
    states = ['q0', 'q1', 'q2', 'q3', 'q4']
    alphabet = ['a', 'b']
    initial_state = 'q0'
    final_states = ['q4']
    transitions = {
        'q0': {'a': {'q1'}, 'b': set()},
        'q1': {'a': {'q2'}, 'b': {'q1'}},
        'q2': {'a': set(), 'b': {'q2', 'q3'}},
        'q3': {'a': {'q1'}, 'b': {'q4'}},
        'q4': {'a': set(), 'b': set()}
    }
    ndfa = NDFA(states, alphabet, transitions, initial_state, final_states)

    # A: FROM NDFA to REGULAR
    print("=== Task a: NDFA to Regular Grammar ===")
    grammar = ndfa.to_regular_grammar()
    grammar.display()

    # B: VERIFICATION
    print("\n=== Task b: DFA or NDFA Check ===")
    if ndfa.is_dfa():
        print("The automaton is deterministic (DFA).")
    else:
        print("The automaton is non-deterministic (NDFA).")

    # C - convversion
    print("\n=== Task c: NDFA to DFA Conversion ===")
    dfa = ndfa.to_dfa()
    dfa.display()