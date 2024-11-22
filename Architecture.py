from abc import ABC, abstractmethod
from dataclasses import dataclass


class Expression(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def __eq__(self, other: object) -> bool:
        pass

    @abstractmethod
    def to_implication_form(self) -> 'Expression':
        pass


@dataclass(frozen=True)
class And(Expression):
    left: Expression
    right: Expression

    def __str__(self) -> str:
        return f"({self.left} ∧ {self.right})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, And) and self.left == other.left and self.right == other.right

    def to_implication_form(self) -> Expression:
        return Negation(Implication(self.left.to_implication_form(), Negation(self.right.to_implication_form())))


@dataclass(frozen=True)
class Implication(Expression):
    left: Expression
    right: Expression

    def __str__(self) -> str:
        return f"({self.left} → {self.right})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Implication) and self.left == other.left and self.right == other.right

    def to_implication_form(self) -> Expression:
        return Implication(self.left.to_implication_form(), self.right.to_implication_form())


@dataclass(frozen=True)
class Negation(Expression):
    expr: Expression

    def __str__(self) -> str:
        return f"¬({self.expr})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Negation) and self.expr == other.expr

    def to_implication_form(self) -> Expression:
        return Negation(self.expr.to_implication_form())


@dataclass(frozen=True)
class Or(Expression):
    left: Expression
    right: Expression

    def __str__(self) -> str:
        return f"({self.left} ∨ {self.right})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Or) and self.left == other.left and self.right == other.right

    def to_implication_form(self) -> Expression:
        return Implication(Negation(self.left.to_implication_form()), self.right.to_implication_form())


@dataclass(frozen=True)
class Xor(Expression):
    left: Expression
    right: Expression

    def __str__(self) -> str:
        return f"({self.left} + {self.right})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Xor) and self.left == other.left and self.right == other.right

    def to_implication_form(self) -> Expression:
        return Or(
            And(Negation(self.left), self.right).to_implication_form(),
            And(self.left, Negation(self.right)).to_implication_form()
        )


@dataclass(frozen=True)
class Equivalence(Expression):
    left: Expression
    right: Expression

    def __str__(self) -> str:
        return f"({self.left} = {self.right})"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Equivalence) and self.left == other.left and self.right == other.right

    def to_implication_form(self) -> Expression:
        return And(
            Implication(self.left.to_implication_form(), self.right.to_implication_form()),
            Implication(self.right.to_implication_form(), self.left.to_implication_form())
        )


@dataclass(frozen=True)
class Variable(Expression):
    name: str

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Variable) and self.name == other.name

    def to_implication_form(self) -> Expression:
        return self


class ExpressionFactory:
    @staticmethod
    def variable(name: str) -> Expression:
        return Variable(name)

    @staticmethod
    def implication(left: Expression, right: Expression) -> Expression:
        return Implication(left, right)

    @staticmethod
    def negation(expr: Expression) -> Expression:
        return Negation(expr)

    @staticmethod
    def conjunction(left: Expression, right: Expression) -> Expression:
        return And(left, right)

    @staticmethod
    def disjunction(left: Expression, right: Expression) -> Expression:
        return Or(left, right)

    @staticmethod
    def exclusive_or(left: Expression, right: Expression) -> Expression:
        return Xor(left, right)

    @staticmethod
    def equivalence(left: Expression, right: Expression) -> Expression:
        return Equivalence(left, right)