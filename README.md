# LFA_Artiom_Bozadji
Formal Languages and Finite Automata

## Laboratory Work '#'5: Chomsky Normal Form
Course: Formal Languages & Finite Automata
Author: Cretu Dumitru and cudos to the Vasile Drumea with Irina Cojuhari
### Always Variant 3

### Objectives:
- [x] Learn about Chomsky Normal Form (CNF)  
  CNF requires all production rules to be of the form \(A \to BC\) (two non-terminals) or \(A \to c\) (single terminal)[2][8]. This standardized form simplifies parsing and analysis[6].

- [x] Get familiar with the approaches of normalizing a grammar  
  Key steps include:  
  1. **Eliminate ε-productions** (e.g., \(A \to \varepsilon\))
  2. **Remove unit productions** (e.g., \(A \to B\))  
  3. **Replace long rules** with chains of binary productions (e.g., \(A \to BCD\) becomes \(A \to BE\), \(E \to CD\))
  4. **Isolate terminals** using helper non-terminals (e.g., \(A \to aB\) becomes \(A \to CB\), \(C \to a\))

- [x] Implement a method for normalizing an input grammar by CNF rules  


### Implementation
# Step-by-Step Explanation

1. **Eliminate ε-Productions**
   Goal: Remove all productions that derive the empty string (ε).
   Process:
   - Identify nullable variables: Variables that can produce ε. Here, only $$\text{C}$$ is nullable due to $$\text{C} \rightarrow \varepsilon$$.
   - Generate new productions: For every production containing a nullable variable, create versions omitting the nullable variable.
     - $$\text{B} \rightarrow \text{aC}$$ becomes $$\text{B} \rightarrow \text{aC} \mid \text{a}$$.
     - $$\text{B} \rightarrow \text{AC}$$ becomes $$\text{B} \rightarrow \text{AC} \mid \text{A}$$.
   - Remove ε-productions: Delete $$\text{C} \rightarrow \varepsilon$$.
   Result:
   - $$\text{C}$$ is kept but has no productions.
   - Updated productions for $$\text{B}$$ include $$\text{a}$$, $$\text{AC}$$, and $$\text{A}$$.

2. **Eliminate Unit Productions (Renaming)**
   Goal: Remove productions of the form $$\text{A} \rightarrow \text{B}$$ (where $$\text{B}$$ is a variable).
   Process:
   - Identify unit pairs: $$\text{S} \rightarrow \text{A}$$ and $$\text{B} \rightarrow \text{A}$$.
   - Replace unit productions: Substitute $$\text{A}$$'s productions into $$\text{S}$$ and $$\text{B}$$.
     - $$\text{S} \rightarrow \text{A}$$ becomes $$\text{S} \rightarrow \text{d} \mid \text{dS} \mid \text{aAdAB}$$.
     - $$\text{B} \rightarrow \text{A}$$ becomes $$\text{B} \rightarrow \text{d} \mid \text{dS} \mid \text{aAdAB}$$.
   Result:
   - All unit productions are replaced by direct terminal or variable sequences.

3. **Eliminate Inaccessible Symbols**
   Goal: Remove variables and terminals unreachable from the start symbol $$\text{S}$$.
   Process:
   - Traverse reachable symbols: Start from $$\text{S}$$ and follow all productions.
   - Identify inaccessible symbols: $$\text{E}$$ is never referenced and is removed.
   Result:
   - $$V_N = \{\text{S, A, B, C}\}$$ (since $$\text{C}$$ is still referenced but has no valid productions).

4. **Eliminate Non-Productive Symbols**
   Goal: Remove variables that cannot derive terminal strings.
   Process:
   - Identify productive symbols: Variables that can produce terminals.
   - Remove non-productive symbols: $$\text{C}$$ has no valid productions and is removed. All productions involving $$\text{C}$$ are deleted.
   Result:
   - $$V_N = \{\text{S, A, B}\}$$.
   - Updated productions exclude any references to $$\text{C}$$.

5. **Final Outptu**
S  → X_d B | X_d | X_d S | Y1 Y3 \
A  → X_d | X_d S | Y1 Y3 \
B  → X_a | X_a S | X_d | X_d S | Y1 Y3 \
X_a → a \
X_d → d \
Y1 → X_a A \
Y2 → Y1 X_d \
Y3 → Y2 A \

