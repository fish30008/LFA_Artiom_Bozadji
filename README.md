**LFA_Artiom_Bozadji
Formal Languages and Finite Automata**

# Report for Laboratory Work '#'1: Regular Grammars & Finite Automata
### Always Variant 3

### Short theory:
*Alphabet Definitions
An alphabet is a finite, nonempty set of
symbols. By convention we use the symbol
 for an alphabet. String (or sometimes a word)
– A finite sequence of symbols chosen from an alphabet.
For example, 010101010 is a string chosen from the binary
alphabet, as is the string 0000 or 1111.
• The empty string  (or “epsilon”) is the string with
zero occurrences of symbols. This string is denoted ε
and may be chosen from any alphabet.
Grammar Definitions
• A grammar G is an ordered quadruple
G=(VN, VT, P, S) where:
VN - is a finite set of non-terminal symbols;
VT - is a finite set of terminal symbols;
VN != VT 
 S is a start symbol;
 P – is a finite set of productions of rules.*
 
 Chomsky Classification
*1. Type 0. Recursively enumerable languages.
Only restriction on rules: left-hand side cannot be the empty
string 
Type 1. Context-Sensitive languages - Context-Sensitive (CS)
rules.
3. Type 2. Context-Free languages - Context-Free (CF) rules
4. Type 3. Regular languages - Non-Context-Free (CF) rules
0 ⊇ 1 ⊇ 2 ⊇ 3
a ⊇ b meaning a properly includes b (a is a superset of b),
i.e. b is a proper subset of a or b is in a*

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
public class Grammar
{
public Grammar(some params...)
public String generateString()
public FiniteAutomaton toFiniteAutomaton()
public class FiniteAutomaton
{
public FiniteAutomaton(constructor params...)
public boolean stringBelongToLanguage(final String inputString)
}
```
Variant 3:
```
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
```


## Main logic of implementation: 
Production = random.choice(self.P[current]) it chooses randomly symbol from dictionary.values() (first is S (aka start))
the main logic of the generating a string is to take the symboll and verifies if it's from Vn, if yes it selects new_string from production again: 
```
                if symbol in self.Vn:
                    new_string += random.choice(self.P[symbol])
                else:
                    new_string += symbol
```
### example of output (Generated strings):
```
fbf
aaafbf
bd
abcd
ff
```

### The string_belongs_to_language method verifies if a given string belongs to the language defined by the finite automaton by iterating over each character of the string, checking for matching transitions from the current state, and updating the state accordingly. If any character does not have a valid transition, the method returns False; otherwise, it returns True after successfully processing all characters.
```
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
```
### Example of output:

```
text = 'abc'

True
```


### Consclusion 
After implementing this labaratory work i learned how to define grammar in programming language, how to iterate through it to generate a string, how to verify if it's a Finite automata and how to verify if string belong to the language. Key point from work is that the start state is used as the initial reference point and does not change during the execution of the automaton. The current state is updated based on the transitions, but the start state remains unchanged. And also if any character does not have a valid transition, then it doesn't belong to our defined language.

