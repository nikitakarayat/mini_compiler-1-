from ast_nodes import BinOp, Num, Var, Assign

class Parser:
    def __init__(self, tokens):
        self.tokens = list(tokens)
        self.pos = 0

    def eat(self, kind):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == kind:
            val = self.tokens[self.pos][1]
            self.pos += 1
            return val
        raise SyntaxError(f'Expected {kind} at position {self.pos}')

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            stmt = self.assignment()
            statements.append(stmt)
        return statements

    def assignment(self):
        name = self.eat('ID')
        self.eat('ASSIGN')
        expr = self.expr()
        return Assign(name, expr)

    def expr(self):
        node = self.term()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('PLUS', 'MINUS'):
            op = self.eat(self.tokens[self.pos][0])
            node = BinOp(node, op, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.pos < len(self.tokens) and self.tokens[self.pos][0] in ('TIMES', 'DIVIDE'):
            op = self.eat(self.tokens[self.pos][0])
            node = BinOp(node, op, self.factor())
        return node

    def factor(self):
        token = self.tokens[self.pos]
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return Num(int(token[1]))
        elif token[0] == 'ID':
            return Var(self.eat('ID'))
        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        raise SyntaxError(f'Unexpected token: {token}')