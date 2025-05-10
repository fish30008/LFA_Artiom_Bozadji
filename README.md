**LFA_Artiom_Bozadji
Formal Languages and Finite Automata**

# Report for Laboratory Work '#'2: Determinism in Finite Automata. Conversion from NDFA 2 DFA. Chomsky Hierarchy.
### Always Variant 3

### Short theory:
Nondeterministic Finite Automaton (NFA)
An NFA is a theoretical model of computation used in formal language theory. 
It consists of: 

A finite set of states ( Q ).

A finite alphabet Σ of input symbols.

A transition function δ:Q×(Σ∪{ε})→2Q is allowing multiple or no next states 
(including ε-transitions, which occur without input).

An initial state q0∈Qq_0 \in Qq_0 \in Q.

A set of final (accepting) states F⊆QF subseteq Q.

NFAs are "nondeterministic" because, for a given state and input, they can transition to multiple states (or none), and ε
-transitions allow spontaneous moves. This flexibility makes NFAs powerful for modeling certain languages but harder to simulate directly.

-------------------------------------------------------------------------------------------------------------------------------------------

Deterministic Finite Automaton (DFA)
A DFA is a restricted version of an NFA with deterministic behavior. It is defined by:
A finite set of states ( Q ).

A finite alphabet Σ.

A transition function δ:Q×Σ→Q, which maps each state and symbol to exactly one next state (no ε-transitions or ambiguity).

An initial state q0∈Qq_0 \in Qq_0 \in Q.

A set of final states F⊆QF subseteq Q.

DFAs are deterministic: at every step, the next state is uniquely determined by the current state and input. While less expressive in definition than NFAs, they recognize the same class of languages (regular languages) and are easier to implement in practice.



NFA to DFA Conversion
The conversion from an NFA to a DFA uses the subset construction method (also called the powerset construction), proving that every language accepted by an NFA is also accepted by some DFA (i.e., they are equivalent in power). The process works as follows:
States: Each DFA state corresponds to a subset of NFA states (QD⊆2^{Q_N}).

Alphabet: Same as the NFA (Σ).

Initial State: The DFA starts with the set containing the NFA’s initial state q0, adjusted 
for ε closures if present (not in our case).

Final States: DFA states containing at least one NFA final state.

The algorithm explores all reachable subsets using a worklist.

Automata theory is the study of abstract
computational devices (abstract state
machine).
• Abstract machine are (simplified) models of
real computations .Automata – plural of “automaton”.
• Finite state automata then a “robot composed of a finite
number of states”
– Informally, a finite list of states with transitions between the states.

### Code structure
```

Class Grammar
Class NDFA
Class DFA
for all defined method display
main logic:
    def to_regular_grammar(self):
    def is_dfa(self):
    def to_dfa(self):
```
Variant 3:
```
Variant 3
Q = {q0,q1,q2,q3,q4},
∑ = {a,b},
F = {q4},
δ(q0,a) = q1,
δ(q1,b) = q1,
δ(q1,a) = q2,
δ(q2,b) = q2,
δ(q2,b) = q3,
δ(q3,b) = q4, 
δ(q3,a) = q1.
```

### a. Implement conversion of a finite automaton to a regular grammar:

Method to_regular_grammar:
Creates a Grammar object.

Sets VN=Q VT=Σ and start=q0.

For each state (q):
For each symbol (a) and next state p∈δ(q,a) adds production q→aq .
If (q) is final, adds q→εq.
Returns the constructed grammar.

### b. Determine whether your FA is deterministic or non-deterministic.

We disscussed about this in short theory part:
A DFA requires that for every state ( q ) and symbol ( a ), δ(q,a) =1 (exactly one next state).
No ε-transitions are allowed (none exist here).
Check each transition:
  q1 -> aq2 | bq1
  q2 -> bq3 | bq2
  q3 -> aq1 | bq4).
Since some transitions violate the condition our FA is non-deterministic

### c. Implement some functionality that would convert an NDFA to a DFA.

Step 1: Convert the given NFA to its equivalent transition table
To convert the NFA to its equivalent transition table, we need to list all the states, input symbols, and the transition rules. The transition rules are represented in the form of a DICTIONARY, where the KEYS represent the current state, the VALUES represent the input symbol, and the cells represent the next state. 

Step 2: Create the DFA’s start state
The DFA’s start state is the set of all possible starting states in the NFA. This set is called the “epsilon closure” of the NFA’s start state. The epsilon closure is the set of all states that can be reached from the start state by following epsilon (?) transitions.

Step 3: Create the DFA’s transition table
The DFA’s transition table is similar to the NFA’s transition table, but instead of individual states, the rows and columns represent sets of states. For each input symbol, the corresponding cell in the transition table contains the epsilon closure of the set of states obtained by following the transition rules in the NFA’s transition table.

Step 4: Create the DFA’s final states
The DFA’s final states are the sets of states that contain at least one final state from the NFA.

### Consclusion 
This work successfully explored the transformation and analysis of a given nondeterministic finite automaton (NFA) through a structured Python implementation. Second, a determinism check confirmed the NFA’s non-deterministic nature due to multiple transitions and undefined moves, distinguishing it from a DFA’s strict single-transition requirement. Third, the subset construction method transformed the NFA into an equivalent DFA, resolving non-determinism by representing states as subsets ensuring a deterministic model that accepts the same regular language.
Theoretically, this process underscores the equivalence of NFAs and DFAs in recognizing regular languages, with the conversion bridging their expressive and operational differences. Practically, the class-based implementation in Python—integrating NDFA, Grammar, and DFA—demonstrates a robust, reusable framework for automata manipulation. This work not only validates the theoretical foundations but also provides a functional toolset for further exploration of formal language concepts, highlighting the power and practicality of automata theory in computational modeling.



