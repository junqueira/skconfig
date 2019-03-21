from abc import ABCMeta, abstractmethod


class Condition(metaclass=ABCMeta):
    def __init__(self, child, parent, conditioned_value):
        self.child = child
        self.parent = parent
        self.conditioned_value = conditioned_value

    @abstractmethod
    def is_active(self, **kwargs):
        ...

    def __and__(self, other):
        conditions = []
        if isinstance(self, AndCondition):
            conditions.extend(self.conditions)
        else:
            conditions.append(self)

        if isinstance(other, AndCondition):
            conditions.extend(other.conditions)
        else:
            conditions.append(other)

        name = {c.child for c in conditions}
        if len(name) != 1:
            raise ValueError("multiple names given: {}".format(name))

        return AndCondition(name.pop(), *conditions)

    def __or__(self, other):
        conditions = []
        if isinstance(self, OrCondition):
            conditions.extend(self.conditions)
        else:
            conditions.append(self)

        if isinstance(other, OrCondition):
            conditions.extend(other.conditions)
        else:
            conditions.append(other)
        name = {c.child for c in conditions}
        if len(name) != 1:
            raise ValueError("multiple names given: {}".format(name))

        return OrCondition(name.pop(), *conditions)


class EqualsCondition(Condition):
    def is_active(self, **kwargs):
        value = kwargs.get(self.parent)
        if value is None:
            return False
        return value == self.conditioned_value

    def __repr__(self):
        return "{} == {}".format(self.parent, self.conditioned_value)


class NotEqualsCondition(Condition):
    def is_active(self, **kwargs):
        value = kwargs.get(self.parent)
        if value is None:
            return False
        return value != self.conditioned_value

    def __repr__(self):
        return "{} != {}".format(self.parent, self.conditioned_value)


class LessThanCondition(Condition):
    def is_active(self, **kwargs):
        value = kwargs.get(self.parent)
        if value is None:
            return True
        return value < self.conditioned_value

    def __repr__(self):
        return "{} < {}".format(self.parent, self.conditioned_value)


class GreaterThanCondition(Condition):
    def is_active(self, **kwargs):
        value = kwargs.get(self.parent)
        if value is None:
            return True
        return value > self.conditioned_value

    def __repr__(self):
        return "{} > {}".format(self.parent, self.conditioned_value)


class InCondition(Condition):
    def is_active(self, **kwargs):
        value = kwargs.get(self.parent)
        if value is None:
            return True
        return value in self.conditioned_value

    def __repr__(self):
        return "{} in {}".format(self.parent, self.conditioned_value)


class AndCondition(Condition):
    def __init__(self, child, *conditions):
        self.child = child
        self.conditions = conditions

    def is_active(self, **kwargs):
        for condition in self.conditions:
            if not condition.is_active(**kwargs):
                return False
        return True

    def __repr__(self):
        return " & ".join(str(c) for c in self.conditions)


class OrCondition(Condition):
    def __init__(self, child, *conditions):
        self.child = child
        self.conditions = conditions

    def is_active(self, **kwargs):
        for condition in self.conditions:
            if condition.is_active(**kwargs):
                return True
        return False

    def __repr__(self):
        return " | ".join(str(c) for c in self.conditions)