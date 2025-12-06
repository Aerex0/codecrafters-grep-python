import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!

def match_token(ch, token, j =1):
    if token == r'\d':
        return ch.isdigit()
    if token == r'\w':
        return ch.isalnum() or ch == '_'
    if token.startswith('[') and token.endswith(']'):
        chars = token[1:-1]
        if chars.startswith('^'):
            return ch not in chars[1:]
        else:
            return ch in chars
    if token.startswith('^'):
        chars = token[1:]
        return ch == chars
    return ch == token

    

def parse_pattern(pattern):
    tokens = []
    i = 0
    while i < len(pattern):
        if pattern[i] == '\\' and i + 1 < len(pattern):
            if pattern[i+1] == 'd':
                tokens.append(r'\d')
                i += 2
                continue
            elif pattern[i+1] == 'w':
                tokens.append(r'\w')
                i += 2
                continue
        elif pattern[i] == '[':
            # find the matching closing bracket
            j = i + 1
            while j < len(pattern) and pattern[j] != ']':
                j += 1
            if j == len(pattern):  # no closing bracket found
                tokens.append('[')
                i += 1
                continue
            tokens.append(pattern[i:j+1])  # full [ ... ]
            i = j + 1
            continue
        tokens.append(pattern[i])
        i += 1
    return tokens


            
    

def match_from(tokens, input_line, start):
    i = start
    for token in tokens:
        if i >= len(input_line):  # ran out of input
            return False
        if not match_token(input_line[i], token):
            return False
        i += 1
    return True

def multi_match_pattern(pattern, input_line):
    tokens = parse_pattern(pattern)
    for start in range(len(input_line) - len(tokens) + 1):
        if match_from(tokens, input_line, start):
            return True
    return False


def match_pattern(pattern, input_line):
    tokens = parse_pattern(pattern)

    if len(tokens) == 1:
        token = tokens[0]
        return any(match_token(ch, token) for ch in input_line)
    else:
        return multi_match_pattern(pattern, input_line)


    

def main():
    pattern = sys.argv[2]
    input_line = sys.stdin.read()

    if sys.argv[1] != "-E":
        print("Expected first argument to be '-E'")
        exit(1)

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!", file=sys.stderr)

    # Uncomment this block to pass the first stage
    if match_pattern(pattern, input_line):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
