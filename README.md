# LFA_Artiom_Bozadji
Formal Languages and Finite Automata

## Laboratory Work '#'1: Regular Grammars & Finite Automata
### Always Variant 3
### Code structure
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

## Main logic of implementation: 
### production = random.choice(self.P[current]) it chooses randomly symbol from dictionary.values() (first is S (star))
### it takes the last word from prodcution (current = production[-1])
### example of output (Generated strings:
aSfRf
fRf
aSaSaSfRf
bDcDcDdRbRf
bDd)
### with string_verification we check if the transition matches the current character and after upday current
