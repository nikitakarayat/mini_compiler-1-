from ast_nodes import Assign, Num, Var, BinOp

def generate(tree):
    env = {}
    output = []

    for stmt in tree:
        if isinstance(stmt, Assign):
            val = eval_expr(stmt.expr, env)
            env[stmt.name] = val
            output.append(f"{stmt.name} = {val}")
    return "\n".join(output)

def eval_expr(node, env):
    if isinstance(node, Num):
        return node.value
    elif isinstance(node, Var):
        return env.get(node.name, 0)
    elif isinstance(node, BinOp):
        left = eval_expr(node.left, env)
        right = eval_expr(node.right, env)
        if node.op == '+':
            return left + right
        elif node.op == '-':
            return left - right
        elif node.op == '*':
            return left * right
        elif node.op == '/':
            return left / right
    return 0
