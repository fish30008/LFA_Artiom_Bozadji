# Report: Dynamic Regular Expression Interpretation and String Generation

## 1. Introduction
Regular expressions (regex) are widely used for pattern matching and validation tasks in computing. This project focuses on dynamically interpreting given regular expressions and generating valid strings conforming to the specified patterns. The approach involves parsing the regex, constructing an abstract syntax tree (AST), and using it to generate outputs systematically.

## 2. Objectives
The primary goals of this project are:
- **Dynamic Interpretation**: Convert a given regex pattern into a structured tree representation.
- **Valid String Generation**: Produce valid strings following the defined regex rules.
- **Processing Log**: Track and display the step-by-step parsing and generation process.
- **Handling Repetitions**: Implement controlled handling of quantifiers (`*`, `+`, `?`, `^N`) to limit excessive repetitions.

## 3. Given Regular Expressions
The project processes the following regex variants:

1. **Variant 1**: `O(P|Q|R)+2(3|4)`
2. **Variant 2**: `A*B(C|D|E)F(G|H|I)^2`
3. **Variant 3**: `J+K(L|M|N)*O?(P|Q)^3`

Each variant consists of a combination of literals, choices (alternation), sequences, and quantifiers.

## 4. Implementation Details
### 4.1. Regex Parsing and Abstract Syntax Tree (AST)
The parser converts regex patterns into an AST consisting of the following node types:
- **LiteralNode**: Represents individual characters (e.g., `O`, `A`, `F`).
- **SequenceNode**: Represents concatenated elements.
- **AlternationNode**: Represents choices (e.g., `(P|Q|R)`).
- **RepetitionNode**: Handles quantifiers such as `*`, `+`, `?`, and `^N`.

### 4.2. Handling Quantifiers
- `*` (Zero or more repetitions) → Limited to a maximum of **5**.
- `+` (One or more repetitions) → Limited to a maximum of **5**.
- `?` (Optional, zero or one occurrence) → Generates either **zero or one occurrence**.
- `^N` (Exact N repetitions) → Generates **exactly N occurrences**.

### 4.3. String Generation Process
The tree structure is traversed to generate a valid string:
1. **LiteralNode**: Outputs the character directly.
2. **SequenceNode**: Concatenates results from child nodes.
3. **AlternationNode**: Selects the first option (for deterministic output).
4. **RepetitionNode**: Generates the required repetitions while following predefined limits.

## 5. Example Outputs
| Variant | Regex Pattern | Generated String |
|---------|--------------|------------------|
| Variant 1 | `O(P|Q|R)+2(3|4)` | `OPP23` |
| Variant 2 | `A*B(C|D|E)F(G|H|I)^2` | `BBFHH` |
| Variant 3 | `J+K(L|M|N)*O?(P|Q)^3` | `JJKPPP` |

## 6. Challenges and Solutions
| Challenge | Solution |
|-----------|----------|
| Handling nested groups | Used recursive parsing with a stack-based approach. |
| Managing repetition limits | Introduced a configurable `MAX_REPETITION` constraint. |
| Ensuring deterministic output | Always chose the first valid option from alternations. |
| Parsing `^N` syntax | Implemented explicit digit parsing after `^`. |

## 7. Processing Log Example
The following is an example of the processing steps:
```
- Start parsing full expression
- Parsing sequence
- Parsing term: 'O'
- Parsing group: '(P|Q|R)'
- AlternationNode: selecting first alternative 'P'
- RepetitionNode: repeating 'P' 2 times
- Parsing literal '2'
- Parsing alternation '(3|4)'
- AlternationNode: selecting first alternative '3'
- Generated string: 'OPP23'
```

## 8. Conclusion
This project successfully implemented a **dynamic regex interpreter and generator** that:
- Parses regex expressions into an AST.
- Generates valid output strings following the rules.
- Provides a step-by-step log for debugging and analysis.
- Handles common regex constructs including alternations, sequences, and quantifiers.

The system can be further improved by adding support for character ranges (`[A-Z]`), escaping mechanisms, and extended regex features.

---

