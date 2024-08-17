class Instruct:
    def __init__(self, opcode: int, value1: int, value2: int, target: int):
        self.opcode = opcode
        self.value1 = value1
        self.value2 = value2
        self.target = target

    def __str__(self):
        return f"""
    Instruct {{
        OPCODE: {self.opcode:08b},
        VALUE1: {self.value1:08b},
        VALUE2: {self.value2:08b},
        TARGET: {self.target:08b}
    }}
        """

    def __repr__(self):
        return str(self)

    def __iter__(self):
        yield self.opcode
        yield self.value1
        yield self.value2
        yield self.target


class InstructionGroup:
    def __init__(self, *instructions: Instruct):
        self.instructions = list(instructions)

    def __str__(self):
        _ = "Instruction Group: \n"
        for i in self.instructions:
            _ += str(i)
        return _

    def __repr__(self):
        return str(self)

    def __getitem__(self, item) -> Instruct:
        return self.instructions[item]

    def __iter__(self):
        return iter(self.instructions)

    @property
    def length(self):
        return len(self.instructions)

    @property
    def code(self):
        return [[i.opcode, i.value1, i.value2, i.target] for i in self.instructions]

    @property
    def bin(self):
        for i in self.instructions:
            yield bytearray(list(i))

    def append(self, *instructions: Instruct):
        self.instructions.extend(instructions)

    def fromByteArray(self, code: bytearray):
        for i in range(0, len(code), 4):
            self.instructions.append(Instruct(code[i], code[i + 1], code[i + 2], code[i + 3]))
