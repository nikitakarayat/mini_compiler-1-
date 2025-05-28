class Num:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return f"Num({self.value})"

class Var:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"Var({self.name})"

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
    def __str__(self):
        return f"BinOp({self.left}, '{self.op}', {self.right})"

class Assign:
    def __init__(self, name, expr):
        self.name = name
        self.expr = expr
    def __str__(self):
        return f"Assign({self.name} = {self.expr})"
