import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!


w_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"



def count(pattern):
    d_count = 0
    w_count = 0
    d_slash = []
    w_slash = []

    length = len(pattern)
    for i in range(length - 1):
         if (pattern[i] == "\\" and pattern[i+1] == "d"):
              d_count+=1
              d_slash.append(i)
         elif (pattern[i] == "\\" and pattern[i+1] == "w"):
              w_count+=1
              w_slash.append(i)
    return d_count,w_count


def match_token(ch, token):
    if token == r'\d':
        return ch.isdigit()
    elif token == r'\w':
        return ch.isalnum() or ch == '_'
    elif token.startswith('[') and token.endswith(']'):
        return ch in token[1:-1]
    else:
        return ch == token
    

def parse_pattern(pattern):
    tokens = [ch for ch in pattern]

    new_tokens = []
    i = 0
    while i < len(tokens):
        if tokens[i] == '\\' and i+1 < len(tokens) and tokens[i+1] == 'd':
            new_tokens.append(r'\d')
            i += 2  # skip the next one because it's already combined
        elif tokens[i] == '\\' and i+1 < len(tokens) and tokens[i+1] == 'w':
            new_tokens.append(r'\w')
            i += 2  # skip the next one because it's already combined
        else:
            new_tokens.append(tokens[i])
            i += 1

    return new_tokens

            
    

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


# ----------------------------------------------------------------------------------------------------

def match_pattern(pattern, input_line):
    d,w = count(pattern)
    if pattern == r"\d":
        return any(char.isdigit() for char in input_line)
    elif pattern == r"\w":
        return any(char in w_characters for char in input_line)
    elif pattern.startswith('[^') and pattern.endswith(']'):
        not_allowed_chars = pattern[2:-1]
        return any(char not in not_allowed_chars for char in input_line) 
    elif pattern.startswith('[') and pattern.endswith(']'):
        allowed_chars = pattern[1:-1]
        return any(char in allowed_chars for char in input_line)
    elif d+w > 1 or len(pattern) > 2:
        return multi_match_pattern(pattern, input_line)
    if len(pattern) == 1:
        return pattern in input_line
    else:
        raise RuntimeError(f"Unhandled pattern: {pattern}")


    

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
