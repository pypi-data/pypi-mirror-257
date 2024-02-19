import typing
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from enum import Enum


class Operation(Enum):
    EQUALS = '=='
    NOT_EQUAL = '!='
    GREATER_THAN = '>'
    GREATER_THAN_OR_EQUAL = '>='
    LESS_THAN = '<='
    LESS_THAN_OR_EQUAL = '<='
    IN = 'in'


@dataclass
class Criteria:  # FIXME - this isn't very fault tolerant at the moment
    key: str
    operation: Operation
    value: typing.Any

    def compare(self, data) -> bool:
        if self.operation == Operation.EQUALS.value:
            return data == self.value
        elif self.operation == Operation.NOT_EQUAL.value:
            return data != self.value
        elif self.operation == Operation.IN.value:
            try:
                return data in self.value
            except TypeError:
                return False
        elif self.operation == Operation.GREATER_THAN.value:
            try:
                return Decimal(data) > Decimal(self.value)
            except (InvalidOperation, TypeError):
                return False
        elif self.operation == Operation.GREATER_THAN_OR_EQUAL.value:
            try:
                return Decimal(data) >= Decimal(self.value)
            except (InvalidOperation, TypeError):
                return False
        elif self.operation == Operation.LESS_THAN.value:
            try:
                return Decimal(data) < Decimal(self.value)
            except (InvalidOperation, TypeError):
                return False
        elif self.operation == Operation.LESS_THAN_OR_EQUAL.value:
            try:
                return Decimal(data) <= Decimal(self.value)
            except (InvalidOperation, TypeError):
                return False


class EmptyStream:
    pass


class ValueNotFound:
    def __gt__(self, other):
        return False

    def __ge__(self, other):
        return False

    def __lt__(self, other):
        return False

    def __le__(self, other):
        return False

    def __eq__(self, other):
        return False

    def __ne__(self, other):
        return True
