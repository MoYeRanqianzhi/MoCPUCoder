from enum import Enum


class AliasWeight:
    OPCODE = 2 ** 24
    VALUE1 = 2 ** 16
    VALUE2 = 2 ** 8
    TARGET = 2 ** 0
    COMPOSE = 2 ** 0
    CONSTANT = 2 ** 0
    NONE = 0

class AliasType(Enum):
    OPCODE = 0
    VALUE1 = 1
    VALUE2 = 2
    TARGET = 3
    COMPOSE = 4
    CONSTANT = 5
    NONE = 6


class Alias:
    def __init__(self, name, code, _type: AliasType = AliasType.NONE):
        self.name = name
        self.code = code
        self.type = _type
        self.weight = AliasWeight.OPCODE if self.type is AliasType.OPCODE else (
            AliasWeight.VALUE1
            if self.type is AliasType.VALUE1
            else (
                AliasWeight.VALUE2
                if self.type is AliasType.VALUE2
                else (
                    AliasWeight.TARGET
                    if self.type is AliasType.TARGET
                    else (
                        AliasWeight.COMPOSE
                        if self.type is AliasType.COMPOSE
                        else (
                            AliasWeight.CONSTANT
                            if self.type is AliasType.CONSTANT
                            else AliasWeight.NONE
                        )
                    )
                )
            )
        )

    def __str__(self):
        return f"{self.name} = {' '.join([format(self.code * self.weight, '032b')[i:i + 8] for i in range(0, 32, 8)])}"

    def __repr__(self):
        return str(self)


class AliasGroup:
    def __init__(self, name="", *aliases: Alias):
        if not len(aliases) == len({_.name for _ in aliases}):
            raise ValueError("重复的别名")

        self.name = name
        self.aliases = list(aliases)

    def __str__(self):
        _ = f"{self.name}:\n"
        for alias in self.aliases:
            _ += f"    {alias}\n"
        return _

    def __repr__(self):
        return str(self)

    def __getitem__(self, item) -> Alias | None:
        try:
            return next(filter(lambda x: x.name == item, self.aliases))
        except StopIteration:
            return None

    def __getattr__(self, item):
        return self[item]

    def __iter__(self) -> Alias:
        for a in self.aliases:
            yield a


standard = AliasGroup(
    "standard",
    Alias("if", 0, AliasType.NONE),
    Alias("else", 0, AliasType.NONE),
    Alias("elif", 0, AliasType.NONE),
    Alias("while", 0, AliasType.NONE),
    Alias("for", 0, AliasType.NONE),
    Alias("in", 0, AliasType.NONE),
    Alias("to", 0, AliasType.NONE),
    Alias("on", 0, AliasType.NONE),
    Alias("with", 0, AliasType.NONE),
    Alias("try", 0, AliasType.NONE),
    Alias("except", 0, AliasType.NONE),
    Alias("finally", 0, AliasType.NONE),

    Alias("MoCPU", 0, AliasType.NONE),
    Alias("v1.1", 0, AliasType.NONE),
    Alias("MoV1", 0, AliasType.NONE),
    Alias("standard", 0, AliasType.NONE),

    Alias("v1", 0b10000000, AliasType.OPCODE),
    Alias("v2", 0b01000000, AliasType.OPCODE),
    Alias("v", 0b11000000, AliasType.OPCODE),

    Alias("ADD", 0, AliasType.OPCODE),
    Alias("SUB", 1, AliasType.OPCODE),
    Alias("MUL", 2, AliasType.OPCODE),
    Alias("DIV", 3, AliasType.OPCODE),
    Alias("F_DIV", 4, AliasType.OPCODE),
    Alias("MOD", 5, AliasType.OPCODE),
    Alias("EXP", 6, AliasType.OPCODE),
    Alias("AND", 7, AliasType.OPCODE),
    Alias("OR", 8, AliasType.OPCODE),
    Alias("XOR", 9, AliasType.OPCODE),

    Alias("true", 32, AliasType.OPCODE),
    Alias("false", 33, AliasType.OPCODE),

    Alias("always", 32, AliasType.OPCODE),
    Alias("never", 33, AliasType.OPCODE),
    Alias("equal", 34, AliasType.OPCODE),
    Alias("not_equal", 35, AliasType.OPCODE),
    Alias("less", 36, AliasType.OPCODE),
    Alias("less_or_equal", 37, AliasType.OPCODE),
    Alias("greater", 38, AliasType.OPCODE),
    Alias("greater_or_equal", 39, AliasType.OPCODE),

    *[Alias(f"*[{i}]", i, AliasType.VALUE1) for i in range(0, 254)],

    Alias("*[ProgramCounter]", 254, AliasType.VALUE1),
    Alias("*[PC]", 254, AliasType.VALUE1),
    Alias("*[pc]", 254, AliasType.VALUE1),
    Alias("*[p]", 254, AliasType.VALUE1),

    Alias("*[input]", 255, AliasType.VALUE1),
    Alias("*[in]", 255, AliasType.VALUE1),
    Alias("*[stdin]", 255, AliasType.VALUE1),

    *[Alias(f"**[{i}]", i, AliasType.VALUE2) for i in range(0, 254)],

    Alias("**[ProgramCounter]", 254, AliasType.VALUE2),
    Alias("**[PC]", 254, AliasType.VALUE2),
    Alias("**[pc]", 254, AliasType.VALUE2),
    Alias("**[p]", 254, AliasType.VALUE2),

    Alias("**[input]", 255, AliasType.VALUE2),
    Alias("**[in]", 255, AliasType.VALUE2),
    Alias("**[stdin]", 255, AliasType.VALUE2),

    *[Alias(f">[{i}]", i, AliasType.VALUE2) for i in range(0, 254)],

    Alias(">[ProgramCounter]", 254, AliasType.TARGET),
    Alias(">[PC]", 254, AliasType.TARGET),
    Alias(">[pc]", 254, AliasType.TARGET),
    Alias(">[p]", 254, AliasType.TARGET),

    Alias(">[output]", 255, AliasType.TARGET),
    Alias(">[out]", 255, AliasType.TARGET),
    Alias(">[stdout]", 255, AliasType.TARGET),
    Alias("[output]", 255, AliasType.TARGET),
    Alias("[out]", 255, AliasType.TARGET),
    Alias("[stdout]", 255, AliasType.TARGET),
    Alias("output", 255, AliasType.TARGET),
    Alias("out", 255, AliasType.TARGET),
    Alias("stdout", 255, AliasType.TARGET),

    *[Alias(f"v1({i})", 0b10000000 * 2 ** 8 + i, AliasType.VALUE1) for i in range(0, 256)],
    *[Alias(f"v2({i})", 0b01000000 * 2 ** 16 + i, AliasType.VALUE2) for i in range(0, 256)],
    *[Alias(f"tar({i})", i, AliasType.TARGET) for i in range(0, 256)],
    *[Alias(f"({i})", i, AliasType.CONSTANT) for i in range(0, 256)],

    Alias("printf", 0b01000000_00000000_00000000_11111111, AliasType.COMPOSE),
    Alias("print", 0b01000000_00000000_00000000_11111111, AliasType.COMPOSE),
    Alias("goto", 0b00100000_00000000_00000000_00000000, AliasType.COMPOSE),
    Alias("jump", 0b00100000_00000000_00000000_00000000, AliasType.COMPOSE),
)


if __name__ == '__main__':
    print(standard)
