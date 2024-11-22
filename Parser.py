import re
from typing import List
from Architecture import *


class Parser:
    OPERATORS = {
        '|': 'disjunction',
        '*': 'conjunction',
        '+': 'exclusive_or',
        '>': 'implication',
        '=': 'equivalence',
        '!': 'negation'
    }
    

    def __init__(self, expression: str):
        self.tokens = self.tokenize(expression)
        self.pos = 0


    @staticmethod
    def tokenize(expression: str) -> List[str]:
        token_pattern = r'\(|\)|\w+|[!|*+=<>]'
        tokens = re.findall(token_pattern, expression)
        return tokens


    def parse(self) -> Expression:
        result = self.parse_equivalence()
        if self.pos < len(self.tokens):
            raise ValueError(f"Неожиданный токен {self.tokens[self.pos]} на позиции {self.pos}")
        return result


    def expect(self, token: str):
        if self.tokens[self.pos] == token:
            self.pos += 1
        else:
            raise ValueError(f"Ожидался '{token}', но найден '{self.tokens[self.pos]}' на позиции {self.pos}")


    def parse_primary(self) -> Expression:
        if self.tokens[self.pos] == '(':
            self.pos += 1
            expr = self.parse_equivalence()
            self.expect(')')
            return expr
        elif self.tokens[self.pos].isalnum():
            return self.parse_variable()
        else:
            raise ValueError(f"Неожиданный токен '{self.tokens[self.pos]}' на позиции {self.pos}")

    def parse_variable(self) -> Expression:
        token = self.tokens[self.pos]
        self.pos += 1
        return ExpressionFactory.variable(token)

    def parse_unary(self) -> Expression:
        if self.tokens[self.pos] == '!':
            self.pos += 1
            return ExpressionFactory.negation(self.parse_unary())
        return self.parse_primary()

    def parse_binary(self, next_parser, operators: str) -> Expression:
        left = next_parser()
        while self.pos < len(self.tokens) and self.tokens[self.pos] in operators:
            operator = self.tokens[self.pos]
            self.pos += 1
            right = next_parser()
            left = getattr(ExpressionFactory, self.OPERATORS[operator])(left, right)
        return left


    def parse_conjunction(self) -> Expression:
        return self.parse_binary(self.parse_unary, '*')


    def parse_disjunction(self) -> Expression:
        return self.parse_binary(self.parse_conjunction, '|')

    def parse_xor(self) -> Expression:
        return self.parse_binary(self.parse_disjunction, '+')


    def parse_implication(self) -> Expression:
        return self.parse_binary(self.parse_xor, '>')


    def parse_equivalence(self) -> Expression:
        return self.parse_binary(self.parse_implication, '=')