import sys

def parse_pattern(pattern):
    tokens = []
    i = 0
    # Handle the start anchor separately if it exists
    is_anchored = False
    is_lineanchored = False
    if pattern.endswith('$'):
        is_lineanchored = True
        pattern = pattern[:-1] # Remove the trailing $
    if pattern.startswith('^'):
        is_anchored = True
        i = 1

    while i < len(pattern):
        if pattern[i] == '\\' and i + 1 < len(pattern):
            tokens.append(pattern[i:i+2]) # Store \d, \w etc.
            i += 2
        elif pattern[i] == '[':
            j = pattern.find(']', i)
            if j == -1:
                tokens.append(pattern[i])
                i += 1
            else:
                tokens.append(pattern[i:j+1])
                i = j + 1
        else:
            tokens.append(pattern[i])
            i += 1
    return tokens, is_anchored, is_lineanchored

def match_token(ch, token):
    if token == r'\d':
        return ch.isdigit()
    if token == r'\w':
        return ch.isalnum() or ch == '_'
    if token.startswith('[') and token.endswith(']'):
        content = token[1:-1]
        if content.startswith('^'):
            return ch not in content[1:]
        return ch in content
    return ch == token

def match_at_position(tokens, input_line, start_pos):
    """Checks if the sequence of tokens matches starting at a specific index."""
    if len(tokens) == 0:
        return True
    
    for j, token in enumerate(tokens):
        input_idx = start_pos + j
        if input_idx >= len(input_line):
            return False
        if not match_token(input_line[input_idx], token):
            return False
    return True

def match_at_position(tokens, input_line, start_pos):
    """Checks if the sequence of tokens matches starting at a specific index."""
    if len(tokens) == 0:
        return True
    
    for j, token in enumerate(tokens):
        input_idx = start_pos + j
        if input_idx >= len(input_line):
            return False
        if not match_token(input_line[input_idx], token):
            return False
        l = -(j+1)
        if not match_token(input_line[-l],token[-l]):
            return False
    return True

def main():
    if len(sys.argv) < 3:
        exit(1)

    pattern = sys.argv[2]
    input_line = sys.stdin.read().strip('\n') # Strip trailing newline from echo

    tokens, is_anchored, is_lineanchored = parse_pattern(pattern)

    if is_anchored or is_lineanchored:
        # Must match exactly from index 0
        if match_at_position(tokens, input_line, 0):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        # Try matching starting at every possible position in the input
        # If the pattern is empty, it usually matches (regex behavior)
        if not tokens:
            sys.exit(0)
            
        for i in range(len(input_line) - len(tokens) + 1):
            if match_at_position(tokens, input_line, i):
                sys.exit(0)
        
        # Special case: allow empty string match if pattern is empty or specific logic requires
        if not input_line and not tokens:
            sys.exit(0)
            
        sys.exit(1)

if __name__ == "__main__":
    main()