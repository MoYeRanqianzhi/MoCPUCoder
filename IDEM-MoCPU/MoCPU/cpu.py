import os
import sys
import time
from typing import IO, TextIO, AnyStr
from instruction import Instruct, InstructionGroup


class MemoryOverflowError(Exception):
    def __init__(self, err: str):
        self.err = "MemoryOverflowError: " + err

    def __str__(self):
        return self.err

    def __repr__(self):
        return self.err


class ProgramCounter:
    _jumpMode = False

    def __init__(self):
        self.pos = 0

    def next(self):
        if not self._jumpMode:
            self.pos += 1
        else:
            self._jumpMode = False

    def jump(self, pos: int):
        self.pos = pos
        self._jumpMode = True


class Registers:
    def __init__(self, p: ProgramCounter, i: IO, o: IO):
        self.p = p
        self.i = i
        self.o = o
        self.registers = [0] * 254

    def __setitem__(self, key, value):
        if key == 254:
            self.p.jump(value)
        elif key == 255:
            self.o.write(value)
            self.o.flush()
        else:
            self.registers[key] = value

    def __getitem__(self, item):
        if item == 254:
            return self.p.pos
        elif item == 255:
            return self.i.read()
        else:
            return self.registers[item]


class AsciiIn(TextIO):
    def read(self, __size: int = -1):
        return ord(sys.stdin.read(1)) & 0xFF


class AsciiOut(TextIO):
    def write(self, __s: AnyStr):
        sys.stdout.write(chr(__s))

    def flush(self):
        sys.stdout.flush()


class UnicodeIn(TextIO):
    def read(self, __size: int = -1):
        return int.from_bytes(sys.stdin.buffer.read(1)) & 0xFF


class UnicodeOut(TextIO):
    buffer = []

    def write(self, __s: AnyStr):
        self.buffer.append(__s)
        sys.stdout.buffer.write(__s.to_bytes(1))

    @property
    def valid(self):
        # check valid utf-8
        if len(self.buffer) == 1:
            return self.buffer[0] & 0b10000000 == 0b00000000  # 1-byte: 0xxxxxxx
        elif len(self.buffer) == 2:
            return (
                    self.buffer[0] & 0b11100000 == 0b11000000 and  # 2-byte: 110xxxxx
                    self.buffer[1] & 0b11000000 == 0b10000000  # 10xxxxxx
            )
        elif len(self.buffer) == 3:
            return (
                    self.buffer[0] & 0b11110000 == 0b11100000 and  # 3-byte: 1110xxxx
                    self.buffer[1] & 0b11000000 == 0b10000000 and  # 10xxxxxx
                    self.buffer[2] & 0b11000000 == 0b10000000  # 10xxxxxx
            )
        elif len(self.buffer) == 4:
            return (
                    self.buffer[0] & 0b11111000 == 0b11110000 and  # 4-byte: 11110xxx
                    self.buffer[1] & 0b11000000 == 0b10000000 and  # 10xxxxxx
                    self.buffer[2] & 0b11000000 == 0b10000000 and  # 10xxxxxx
                    self.buffer[3] & 0b11000000 == 0b10000000  # 10xxxxxx
            )
        else:
            return False

    def flush(self):
        if self.valid:
            self.buffer.clear()
            sys.stdout.buffer.flush()


class MoCPU:
    def __init__(self, p: ProgramCounter, i: IO, o: IO, tick=0.0):
        self.p = p
        self.i = i
        self.o = o
        self.registers = Registers(p, i, o)
        self.operations = {
            0: lambda a, b: (a + b) & 0xFF,
            1: lambda a, b: (a - b) & 0xFF,
            2: lambda a, b: (a * b) & 0xFF,
            3: lambda a, b: (a / b) & 0xFF,
            4: lambda a, b: (a // b) & 0xFF,
            5: lambda a, b: (a % b) & 0xFF,
            6: lambda a, b: (a ** b) & 0xFF,
            7: lambda a, b: (a & b) & 0xFF,
            8: lambda a, b: (a | b) & 0xFF,
            9: lambda a, b: (a ^ b) & 0xFF,

            32: lambda a, b: True,
            33: lambda a, b: False,
            34: lambda a, b: a == b,
            35: lambda a, b: a != b,
            36: lambda a, b: a < b,
            37: lambda a, b: a <= b,
            38: lambda a, b: a > b,
            39: lambda a, b: a >= b,
        }

        self.tick = tick

    @staticmethod
    def syntaxCheck(opcode: int, value1: int, value2: int, target: int):
        if opcode > 255:
            raise MemoryOverflowError("OPCODE > 255, should be >= 0 and <= 255")
        if opcode < 0:
            raise MemoryOverflowError("OPCODE < 0, should be >= 0 and <= 255")
        if value1 > 255:
            raise MemoryOverflowError("VALUE1 > 255, should be >= 0 and <= 255")
        if value1 < 0:
            raise MemoryOverflowError("VALUE1 < 0, should be >= 0 and <= 255")
        if value2 > 255:
            raise MemoryOverflowError("VALUE2 > 255, should be >= 0 and <= 255")
        if value2 < 0:
            raise MemoryOverflowError("VALUE2 < 0, should be >= 0 and <= 255")
        if target > 255:
            raise MemoryOverflowError("TARGET > 255, should be >= 0 and <= 255")
        if target < 0:
            raise MemoryOverflowError("TARGET < 0, should be >= 0 and <= 255")

    def run(self, code: list[[int, int, int, int]]):
        """
        Parameters:
            code = list[[0, 0, 0, 0], [0, 0, 0, 255]]
        """
        while self.p.pos < len(code):
            self.exec(code[self.p.pos][0], code[self.p.pos][1], code[self.p.pos][2], code[self.p.pos][3])
            self.p.next()

            if self.tick:
                time.sleep(self.tick)

    def exec(self, opcode: int, value1: int, value2: int, target: int):
        self.syntaxCheck(opcode, value1, value2, target)

        op = self.operations[opcode & 0b0011_1111]
        v1 = value1 if opcode & 128 else self.registers[value1]
        v2 = value2 if opcode & 64 else self.registers[value2]

        if not opcode & 32:
            self.cal(op, v1, v2, target)
        else:
            self.cond(op, v1, v2, target)

    def cal(self, calculation: callable, value1: int, value2: int, target: int):
        self.registers[target] = calculation(value1, value2)

    def cond(self, condition: callable, value1: int, value2: int, target: int):
        if condition(value1, value2):
            self.p.jump(target)


if __name__ == '__main__':
    if os.path.exists(sys.argv[1]):
        m = MoCPU(ProgramCounter(), UnicodeIn(), UnicodeOut(), 0.1)
        ig = InstructionGroup()
        with open(sys.argv[1], "rb") as f:
            ig.fromByteArray(bytearray(f.read()))
        m.run(ig.code)
    # m = MoCPU(ProgramCounter(), UnicodeIn(), UnicodeOut(), 0.1)
    # c = InstructionGroup(
    #     Instruct(192, 228, 0, 255),
    #     Instruct(192, 189, 0, 255),
    #     Instruct(192, 160, 0, 255),
    #     Instruct(192, 229, 0, 255),
    #     Instruct(192, 165, 0, 255),
    #     Instruct(192, 189, 0, 255),
    #     Instruct(192, 239, 0, 255),
    #     Instruct(192, 188, 0, 255),
    #     Instruct(192, 140, 0, 255),
    #     Instruct(192, 228, 0, 255),
    #     Instruct(192, 184, 0, 255),
    #     Instruct(192, 150, 0, 255),
    #     Instruct(192, 231, 0, 255),
    #     Instruct(192, 149, 0, 255),
    #     Instruct(192, 140, 0, 255),
    # )
    # m.run(c.code)
