import re

def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+'),
        ('ASSIGN',   r'='),
        ('PLUS',     r'\+'),
        ('MINUS',    r'-'),
        ('TIMES',    r'\*'),
        ('DIVIDE',   r'/'),
        ('LPAREN',   r'\('),
        ('RPAREN',   r'\)'),
        ('ID',       r'[A-Za-z]+'),
        ('SKIP',     r'[ \t]+'),
        ('MISMATCH', r'.')
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NUMBER':
            yield ('NUMBER', value)
        elif kind == 'ID':
            yield ('ID', value)
        elif kind == 'ASSIGN':
            yield ('ASSIGN', value)
        elif kind in ('PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN'):
            yield (kind, value)
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'Unexpected character: {value}')