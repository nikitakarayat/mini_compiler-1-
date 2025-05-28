from lexer import tokenize
from parser import Parser
from codegen import generate

def main():
    with open("test.txt") as f:
        code = f.read()

    tokens = list(tokenize(code))
    parser = Parser(tokens)
    tree = parser.parse()

    result = generate(tree)
    print("Generated Code:\n", result)

    with open("output.txt", "w") as out:
        out.write(result)

if __name__ == "__main__":
    main()