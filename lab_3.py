class Token:
    # EOF (end of file)
    TOK_EOF = -1

    # SQL Keywords
    TOK_SELECT = -2
    TOK_FROM = -3
    TOK_WHERE = -4
    TOK_ORDER = -5
    TOK_BY = -6
    TOK_GROUP = -7
    TOK_HAVING = -8
    TOK_AS = -9
    TOK_JOIN = -10
    TOK_ON = -11
    TOK_AND = -12
    TOK_OR = -13
    TOK_NOT = -14
    TOK_IN = -15
    TOK_LIKE = -16

    # Types
    TOK_IDENTIFIER = -100  # Table or column names
    TOK_NUMBER = -101  # Numeric literals
    TOK_STRING = -102  # String literals

    # Operators
    TOK_OPERATOR = -200  # General operator token


class SQLLexer:
    def __init__(self, input_text):
        self.input = input_text

        # Keywords mapping for easy lookup (case-insensitive)
        self.keywords = {
            "SELECT": Token.TOK_SELECT,
            "FROM": Token.TOK_FROM,
            "WHERE": Token.TOK_WHERE,
            "ORDER": Token.TOK_ORDER,
            "BY": Token.TOK_BY,
            "GROUP": Token.TOK_GROUP,
            "HAVING": Token.TOK_HAVING,
            "AS": Token.TOK_AS,
            "JOIN": Token.TOK_JOIN,
            "ON": Token.TOK_ON,
            "AND": Token.TOK_AND,
            "OR": Token.TOK_OR,
            "NOT": Token.TOK_NOT,
            "IN": Token.TOK_IN,
            "LIKE": Token.TOK_LIKE
        }

        # List of operators
        self.operators = ['+', '-', '*', '/', '=', '!=', '<>', '<', '>', '<=', '>=',
                          '(', ')', ',', ';', '.']

        # Special characters that should be treated as separate tokens
        self.special_chars = "+-*/=<>(),.;'"

    def preprocess_for_split(self):
        """
        Preprocesses the SQL string to handle operators and special characters
        before splitting.
        """
        # First handle string literals - replace spaces within quotes temporarily
        processed = ""
        in_string = False
        i = 0

        while i < len(self.input):
            char = self.input[i]

            if char == "'":
                # Toggle string mode
                in_string = not in_string
                processed += char
            elif in_string and char == " ":
                # Replace spaces in strings with a special marker
                processed += "here_was_space"
            elif not in_string and char in self.special_chars:
                # Add spaces around special characters when not in a string
                processed += f" {char} "
            else:
                processed += char

            i += 1

        # Handle special multi-character operators
        for op in ['<=', '>=', '!=', '<>']:
            # Replace the spaced version with a non-spaced version
            spaced_op = ' '.join(op)
            processed = processed.replace(f" {spaced_op} ", f" {op} ")

        return processed

    def is_number(self, token):
        """Check if a token is a number"""
        try:
            # Try to convert to float
            float(token)
            return True
        except ValueError:
            return False

    def tokenize(self):
        """Tokenize the SQL query using split method"""
        # Preprocess the SQL query
        processed_sql = self.preprocess_for_split()

        # Remove SQL comments
        lines = processed_sql.split('\n')
        clean_lines = []

        for line in lines:
            comment_pos = line.find('--')
            if comment_pos != -1:
                line = line[:comment_pos]
            if line.strip():  # Only add non-empty lines
                clean_lines.append(line)

        processed_sql = ' '.join(clean_lines)

        # Split into tokens (words and special characters)
        raw_tokens = processed_sql.split()

        # Process each token
        tokens = []

        for token in raw_tokens:
            # Restore spaces in string literals
            token = token.replace("here_was_space", " ")

            # Check if it's a string literal (surrounded by quotes)
            if token.startswith("'") and token.endswith("'") and len(token) >= 2:
                # Remove the quotes
                string_value = token[1:-1]
                tokens.append((Token.TOK_STRING, string_value))

            # Check if it's an operator
            elif token in self.operators:
                tokens.append((Token.TOK_OPERATOR, token))

            # Check if it's a number
            elif self.is_number(token):
                # Convert to appropriate numeric type
                if '.' in token:
                    value = float(token)
                else:
                    value = int(token)
                tokens.append((Token.TOK_NUMBER, value))

            else:
                upper_token = token.upper()
                if upper_token in self.keywords:
                    tokens.append((self.keywords[upper_token], token))
                else:
                    tokens.append((Token.TOK_IDENTIFIER, token))

        # Add EOF token
        tokens.append((Token.TOK_EOF, "EOF"))

        return tokens


def token_name(token_type):
    token_names = {
        Token.TOK_EOF: "EOF",
        Token.TOK_SELECT: "SELECT",
        Token.TOK_FROM: "FROM",
        Token.TOK_WHERE: "WHERE",
        Token.TOK_ORDER: "ORDER",
        Token.TOK_BY: "BY",
        Token.TOK_GROUP: "GROUP",
        Token.TOK_HAVING: "HAVING",
        Token.TOK_AS: "AS",
        Token.TOK_JOIN: "JOIN",
        Token.TOK_ON: "ON",
        Token.TOK_AND: "AND",
        Token.TOK_OR: "OR",
        Token.TOK_NOT: "NOT",
        Token.TOK_IN: "IN",
        Token.TOK_LIKE: "LIKE",
        Token.TOK_IDENTIFIER: "IDENTIFIER",
        Token.TOK_NUMBER: "NUMBER",
        Token.TOK_STRING: "STRING",
        Token.TOK_OPERATOR: "OPERATOR"
    }
    return token_names.get(token_type, f"UNKNOWN({token_type})")


# Example usage
def test_lexer():
    sql_query = """
    SELECT id, first_name, last_name, salary + bonus AS total_compensation
    FROM employees 
    """

    lexer = SQLLexer(sql_query)
    tokens = lexer.tokenize()

    print(type(tokens))
    print(tokens[1])
    for token_type, token_value in tokens:
        print(f"Token: {token_name(token_type)}, Value: {token_value}")


if __name__ == "__main__":
    test_lexer()