from collections import deque


class Grammar:
    def __init__(self, VN, VT, P, S):
        self.VN = set(VN)
        self.VT = set(VT)
        self.P = {k: [list(p) for p in v] for k, v in P.items()}
        self.S = S

    def eliminate_epsilon(self):
        # Step 1: Find all nullable variables
        nullable = set()
        for var in self.VN:
            for prod in self.P.get(var, []):
                if prod == ['e']:
                    nullable.add(var)
        changed = True
        while changed:
            changed = False
            for var in self.VN:
                for prod in self.P.get(var, []):
                    if all(sym in nullable or sym == 'e' for sym in prod):
                        if var not in nullable:
                            nullable.add(var)
                            changed = True
        # Generate new productions by omitting nullable symbols
        new_P = {v: [] for v in self.VN}
        for var in self.VN:
            for prod in self.P.get(var, []):
                if prod == ['e']:
                    continue
                indices = [i for i, sym in enumerate(prod) if sym in nullable]
                from itertools import chain, combinations
                all_combinations = []
                for r in range(len(indices) + 1):
                    for subset in combinations(indices, r):
                        all_combinations.append(subset)
                seen = set()
                for subset in all_combinations:
                    new_prod = [sym for i, sym in enumerate(prod) if i not in subset or sym not in nullable]
                    if not new_prod:
                        if var not in new_P:
                            new_P[var] = []
                        new_P[var].append(['e'])
                    else:
                        tp = tuple(new_prod)
                        if tp not in seen:
                            seen.add(tp)
                            new_P[var].append(new_prod)
        # Remove epsilon productions and update
        self.P = new_P
        for var in list(self.P.keys()):
            self.P[var] = [p for p in self.P[var] if p != ['e']]
            if not self.P[var]:
                del self.P[var]
        # Remove 'e' from any productions
        for var in self.P:
            for i in range(len(self.P[var])):
                self.P[var][i] = [sym for sym in self.P[var][i] if sym != 'e']
        # Remove variables that have no productions
        self.VN = set(self.P.keys())

    def eliminate_unit(self):
        # Find all unit productions
        units = {}
        for var in self.VN:
            units[var] = set()
            for prod in self.P.get(var, []):
                if len(prod) == 1 and prod[0] in self.VN:
                    units[var].add(prod[0])
        # Compute closure of unit pairs
        changed = True
        while changed:
            changed = False
            for A in units:
                for B in list(units[A]):
                    for C in units.get(B, []):
                        if C not in units[A]:
                            units[A].add(C)
                            changed = True
        # Replace unit productions
        new_P = {v: [] for v in self.VN}
        for var in self.VN:
            for prod in self.P.get(var, []):
                if len(prod) == 1 and prod[0] in self.VN:
                    continue  # Skip unit productions
                new_P[var].append(prod)
            # Add all productions from unit closure
            if var in units:
                for B in units[var]:
                    for prod in self.P.get(B, []):
                        if len(prod) == 1 and prod[0] in self.VN:
                            continue  # Skip adding further unit productions
                        if prod not in new_P[var]:
                            new_P[var].append(prod)
        self.P = new_P

    def eliminate_inaccessible(self):
        accessible = set([self.S])
        queue = deque([self.S])
        while queue:
            current = queue.popleft()
            for prod in self.P.get(current, []):
                for sym in prod:
                    if sym in self.VN and sym not in accessible:
                        accessible.add(sym)
                        queue.append(sym)
        # Remove inaccessible variables
        self.VN = set([v for v in self.VN if v in accessible])
        self.P = {k: v for k, v in self.P.items() if k in accessible}
        # Also remove inaccessible symbols from productions
        for var in self.P:
            new_prods = []
            for prod in self.P[var]:
                if all(sym in self.VT or sym in self.VN for sym in prod):
                    new_prods.append(prod)
            self.P[var] = new_prods

    def eliminate_non_productive(self):
        # Find productive variables (can derive terminals)
        productive = set()
        for var in self.VN:
            for prod in self.P.get(var, []):
                if all(sym in self.VT for sym in prod):
                    productive.add(var)
                    break
        changed = True
        while changed:
            changed = False
            for var in self.VN:
                if var in productive:
                    continue
                for prod in self.P.get(var, []):
                    if all(sym in self.VT or sym in productive for sym in prod):
                        productive.add(var)
                        changed = True
                        break
        # Remove non-productive variables
        self.VN = set(productive)
        self.P = {k: [prod for prod in v if all(sym in self.VT or sym in productive for sym in prod)] for k, v in
                  self.P.items() if k in productive}

    def to_cnf(self):
        # Step 1: Introduce new variables for terminals
        term_var = {}
        for t in self.VT:
            term_var[t] = f'X_{t}'
        new_VN = list(self.VN) + list(term_var.values())
        new_P = {k: [p.copy() for p in v] for k, v in self.P.items()}
        # Add terminal replacement productions
        for t, var in term_var.items():
            new_P[var] = [[t]]
        # Replace terminals in productions with length >=2
        for var in list(new_P.keys()):
            prods = new_P[var]
            new_prods = []
            for prod in prods:
                if len(prod) <= 1:
                    new_prods.append(prod)
                    continue
                new_prod = []
                for sym in prod:
                    if sym in self.VT:
                        new_prod.append(term_var[sym])
                    else:
                        new_prod.append(sym)
                new_prods.append(new_prod)
            new_P[var] = new_prods
        # Step 2: Break productions with length >2 into binary
        current_VN = set(new_VN)
        y_count = 1
        for var in list(new_P.keys()):
            new_prods = []
            for prod in new_P[var]:
                if len(prod) <= 2:
                    new_prods.append(prod)
                    continue
                # Need to break into binary
                current = prod[0]
                for i in range(1, len(prod) - 1):
                    new_var = f'Y{y_count}'
                    y_count += 1
                    current_VN.add(new_var)
                    new_P[new_var] = [[current, prod[i]]]
                    current = new_var
                new_prod = [current, prod[-1]]
                new_prods.append(new_prod)
            new_P[var] = new_prods
        # Update the grammar
        self.VN = current_VN
        self.P = new_P

    def get_cnf(self):
        self.eliminate_epsilon()
        self.eliminate_unit()
        self.eliminate_inaccessible()
        self.eliminate_non_productive()
        self.to_cnf()
        return {
            'VN': self.VN,
            'VT': self.VT,
            'P': {k: [tuple(p) for p in v] for k, v in self.P.items()},
            'S': self.S
        }


# Testing the given grammar
VN = {'S', 'A', 'B', 'C', 'E'}
VT = {'a', 'd'}
P = {
    'S': [['d', 'B'], ['A']],
    'A': [['d'], ['d', 'S'], ['a', 'A', 'd', 'A', 'B']],
    'B': [['a', 'C'], ['a', 'S'], ['A', 'C']],
    'C': [['e']],
    'E': [['A', 'S']]
}
S = 'S'

grammar = Grammar(VN, VT, P, S)
cnf_grammar = grammar.get_cnf()

# Print the result
print("CNF Grammar:")
print("VN:", cnf_grammar['VN'])
print("VT:", cnf_grammar['VT'])
print("P:")
for var in sorted(cnf_grammar['P']):
    prods = [' '.join(p) if p else 'ε' for p in cnf_grammar['P'][var]]
    print(f"{var} -> {' | '.join(prods)}")
print("S:", cnf_grammar['S'])