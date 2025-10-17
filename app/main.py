import sys

# import pyparsing - available if you need it!
# import lark - available if you need it!

w_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_"

def match_pattern(input_line, pattern):
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
    if match_pattern(input_line, pattern):
        exit(0)
    else:
        exit(1)


if __name__ == "__main__":
    main()
