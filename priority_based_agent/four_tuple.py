from dataclasses import dataclass


@dataclass
class FourTuple:
    zero: int
    one: int
    two: int
    three: int

    def __getitem__(self, index: int):
        if index == 0: return self.zero
        elif index == 1: return self.one
        elif index == 2: return self.two
        elif index == 3: return self.three
        else: raise KeyError('key must be between 0 and 3')

    def __setitem__(self, index: int, value: int):
        if index == 0: self.zero = value
        elif index == 1: self.one = value
        elif index == 2: self.two = value
        elif index == 3: self.three = value
        else: raise KeyError('key must be between 0 and 3')

    def __hash__(self):
        return hash(self.zero) ^ hash(self.one) ^ hash(self.two) ^ hash(self.three)

    def __str__(self):
        return f'4-tuple({self.zero}, {self.one}, {self.two}, {self.three})'

    def __contains__(self, item: int):
        return item in [self.zero, self.one, self.two, self.three]


def invert_4_tuple(t: FourTuple) -> FourTuple:
    def invert_number(n: int):
        if n == 0: return 0
        if n == 1: return 2
        if n == 2: return 1

    return FourTuple(
        invert_number(t.zero),
        invert_number(t.one),
        invert_number(t.two),
        invert_number(t.three)
    )
