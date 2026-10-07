"""
Парсинг выражений
"""

from ast_nodes import BinaryOp, UnaryOp
from .base import Parser


def parse_expression(self):
    return self.parse_or()


def parse_or(self):
    left = self.parse_and()
    while self.check('OR'):
        self.expect('OR')
        right = self.parse_and()
        left = BinaryOp('OR', left, right)
    return left


def parse_and(self):
    left = self.parse_not()
    while self.check('AND'):
        self.expect('AND')
        right = self.parse_not()
        left = BinaryOp('AND', left, right)
    return left


def parse_not(self):
    if self.check('NOT'):
        self.expect('NOT')
        right = self.parse_not()
        return UnaryOp('NOT', right)
    return self.parse_comparison()


def parse_comparison(self):
    left = self.parse_add()
    while self.peek() and self.peek()[0] in ['EQUALS', 'NOTEQUAL', 'LESS', 'GREATER', 'LESSEQUAL', 'GREATEREQUAL']:
        op = self.expect(self.peek()[0])[0]
        right = self.parse_add()
        left = BinaryOp(op, left, right)
    return left


def parse_add(self):
    left = self.parse_mul()
    while self.check('PLUS') or self.check('MINUS'):
        op = self.expect(self.peek()[0])[0]
        right = self.parse_mul()
        left = BinaryOp(op, left, right)
    return left


def parse_mul(self):
    left = self.parse_pow()
    while self.check('STAR') or self.check('SLASH') or self.check('MOD') or self.check('FLOORDIV'):
        op = self.expect(self.peek()[0])[0]
        right = self.parse_pow()
        left = BinaryOp(op, left, right)
    return left


def parse_pow(self):
    left = self.parse_unary()
    while self.check('POW'):
        op = self.expect('POW')[0]
        right = self.parse_unary()
        left = BinaryOp(op, left, right)
    return left


def parse_unary(self):
    if self.check('MINUS'):
        op = self.expect('MINUS')[0]
        right = self.parse_unary()
        return UnaryOp(op, right)
    return self.parse_primary()