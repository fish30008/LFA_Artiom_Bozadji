import random

MAX_REPETITION = 5
class RegexNode:
    def generate(self, log):
        raise NotImplementedError("generate() must be implemented.")

    # method string prints when we are innaciate the class
    def __str__(self):
        raise NotImplementedError("__str__() must be implemented.")


# Node representing a literal character.
class LiteralNode(RegexNode):
    def __init__(self, literal):
        self.literal = literal

    def generate(self, log):
        log.append(f"LiteralNode: returning '{self.literal}'")
        return self.literal

    def __str__(self):
        return self.literal

class SequenceNode(RegexNode):
    def __init__(self, nodes):
        self.nodes = nodes

    def generate(self, log):
        log.append("SequenceNode: processing sequence")
        result = ""
        for node in self.nodes:
            part = node.generate(log)
            result += part
        log.append(f"SequenceNode: result = '{result}'")
        return result

    def __str__(self):
        return "".join(str(node) for node in self.nodes)

# to parse groups
class AlternationNode(RegexNode):
    def __init__(self, options):
        self.options = options

    def generate(self, log):
        log.append("AlternationNode: choosing an alternative")
        chosen = random.choice(self.options)
        return chosen.generate(log)

    def __str__(self):
        return "(" + "|".join(str(option) for option in self.options) + ")"


# To parse the repetitions
class RepetitionNode(RegexNode):
    def __init__(self, node, min_rep, max_rep):
        self.node = node
        self.min_rep = min_rep
        self.max_rep = max_rep

    def generate(self, log):
        log.append(f"RepetitionNode: repeating between {self.min_rep} and {self.max_rep} times")
        count = random.randint(self.min_rep, self.max_rep)
        result = ""
        part = self.node.generate(log)
        for i in range(count):

            result += part
        log.append(f"RepetitionNode: generated '{result}' with {count} repetitions")
        return result

    def __str__(self):
        if self.min_rep == 0 and self.max_rep == MAX_REPETITION:
            return str(self.node) + "*"
        elif self.min_rep == 1 and self.max_rep == MAX_REPETITION:
            return str(self.node) + "+"
        elif self.min_rep == 0 and self.max_rep == 1:
            return str(self.node) + "?"
        elif self.min_rep == self.max_rep:
            return str(self.node) + "^" + str(self.min_rep)
        else:
            return str(self.node) + "{" + f"{self.min_rep},{self.max_rep}" + "}"


# Main build parser
class RegexParser:
    def __init__(self, pattern):
        self.pattern = pattern
        self.pos = 0
        self.log = []

    def current(self):
        if self.pos < len(self.pattern):
            return self.pattern[self.pos]
        return None

    def eat(self, ch):
        if self.current() == ch:
            self.log.append(f"Eating  '{ch}' at position {self.pos}")
            self.pos += 1
        else:
            raise ValueError(f"Expected '{ch}' at position {self.pos}")

    def parse(self):
        self.log.append("Start parsing full expression")
        node = self.parse_sequence()
        self.log.append("Finished parsing full expression")
        return node

    def parse_sequence(self):
        nodes = []
        self.log.append("Parsing sequence")
        while self.pos < len(self.pattern) and self.current() not in [')', '|']:
            node = self.parse_term()
            nodes.append(node)
        if len(nodes) == 1:
            return nodes[0]
        return SequenceNode(nodes)

    def parse_term(self):
        self.log.append(f"Parsing term at pos {self.pos}")
        node = self.parse_factor()
        if self.current() in ['*', '+', '?', '^']:
            node = self.parse_symbol (node)
        return node

    def parse_factor(self):
        ch = self.current()
        self.log.append(f"Parsing factor at pos {self.pos}: '{ch}'")
        if ch == '(':
            return self.parse_group()
        else:
            self.pos += 1
            return LiteralNode(ch)

    def parse_group(self):
        self.log.append(f"Parsing group starting at pos {self.pos}")
        self.eat('(')
        options = []
        options.append(self.parse_sequence())
        # Parse alternatives separated by '|'
        while self.current() == '|':
            self.eat('|')
            options.append(self.parse_sequence())
        self.eat(')')
        if len(options) == 1:
            group_node = options[0]
        else:
            group_node = AlternationNode(options)
        self.log.append("Finished parsing group")
        if self.current() in ['*', '+', '?', '^']:
            group_node = self.parse_symbol (group_node)
        return group_node

    def parse_symbol (self, node):
        ch = self.current()
        self.log.append(f"Parsing symbol  '{ch}' at pos {self.pos}")
        if ch == '*':
            self.pos += 1
            return RepetitionNode(node, 0, MAX_REPETITION)
        elif ch == '+':
            self.pos += 1
            return RepetitionNode(node, 1, MAX_REPETITION)
        elif ch == '?':
            self.pos += 1
            return RepetitionNode(node, 0, 1)
        elif ch == '^':
            self.pos += 1
            digits = ""
            while self.current() is not None and self.current().isdigit():
                digits += self.current()
                self.pos += 1
            if not digits:
                raise ValueError("Expected digit(s) after '^'")
            count = int(digits)
            return RepetitionNode(node, count, count)
        else:
            return node


def generate_from_regex(regex_pattern):
    parser = RegexParser(regex_pattern)
    root = parser.parse()
    generation_log = []
    result = root.generate(generation_log)
    return result, parser.log + generation_log


# Define our three variants.
regex_variants = {
    1: "O(P|Q|R)+2(3|4)",
    2: "A*B(C|D|E)F(G|H|I)^2",
    3: "J+K(L|M|N)*O?(P|Q)^3"
}

# Process each variant.
for variant, pattern in regex_variants.items():
    print(f"--- {variant} ---")
    print("Regex Pattern:")
    print(pattern)
    print()
    try:
        generated_str, process_log = generate_from_regex(pattern)
        print("Generated String:")
        print(generated_str)
        print()
        print("Processing Log:")
        for entry in process_log:
            print("  -", entry)
    except Exception as e:
        print("Error:", e)
    print("-" * 40)

