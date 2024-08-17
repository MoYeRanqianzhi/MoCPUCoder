import os.path
import sys
import time

from alias import Alias, AliasType, AliasGroup, AliasWeight, standard
from instruction import Instruct, InstructionGroup
from abc import abstractmethod
import re


class Logger:
    @abstractmethod
    def log(self, *messages):
        print(*[str(msg) for msg in messages])

    @abstractmethod
    def err(self, *messages: str):
        time.sleep(0.5)
        sys.stderr.write("\033[31m" + "\n".join(messages) + "\033[0m")
        sys.stderr.flush()
        sys.exit(-1)


class CompilerBase:
    __copyright__ = "Copyright (c) 2024, MoCPU by MoYeRanSoft (墨叶染千枝) - (墨软)"

    @abstractmethod
    def compile(self, code: str) -> InstructionGroup:
        pass


class Compiler:
    def __init__(self, ag: AliasGroup = standard, logger: Logger = Logger()):
        self.ag = ag
        self.logger = logger

    def compile(self, code: str) -> InstructionGroup:
        ig = InstructionGroup()

        self.logger.log("[DECODE]", "正在开始解码")
        lines = self.decode(code)
        self.logger.log("[DECODE]", "解码完成")

        self.logger.log("[CONST+MARK]", "开始解析常量")
        constants = {}
        num = 0  # 常量定义出现次数
        for line, lineno in zip(lines.copy(), range(len(lines.copy()))):
            if line[0] in ["const", "CONST", "mark", "MARK"]:
                if len(line) == 4:
                    if all(
                            [
                                line[0] in ["const", "CONST"],
                                re.match(r"[a-zA-Z_]\w*$", line[1]),
                                line[2] == "=",
                                re.match(r"0[bB][01]+|0[xX][a-fA-F0-9]+|\d+$", line[3])
                            ]
                    ):
                        if line[1] in constants:
                            self.logger.log(
                                f"[{lineno}]",
                                "WARNING!",
                                "常量(标记)定义重复!",
                                "重复定义是无效的行为~",
                                f"已有: {line[1]} = {constants[line[1]]}"
                            )

                        constants.update(
                            {
                                line[1]: int(line[3], 0)
                            }
                        )
                        lines.pop(lineno - num)
                        num += 1
                        self.logger.log(
                            f"[{lineno}]",
                            f"定义常量: {line[1]} = {constants[line[1]]}"
                        )

                    else:
                        self.logger.log(
                            f"[{lineno}]",
                            "ERROR?",
                            "WARNING!!!",
                            "无匹配常量语法,",
                            "但是似乎此处应定义常量或标记!"
                        )

                elif len(line) == 2:
                    if all(
                            [
                                line[0] in ["mark", "MARK"],
                                re.match(r"[a-zA-Z_]\w*$", line[1])
                            ]
                    ):
                        if line[1] in constants:
                            self.logger.log(
                                f"[{lineno}]",
                                "WARNING!",
                                "标记(常量)定义重复!",
                                "重复定义是无效的行为~",
                                f"已有: {line[1]} = {constants[line[1]]}"
                            )

                        constants.update(
                            {
                                line[1]: lineno - num
                            }
                        )
                        lines.pop(lineno - num)
                        num += 1
                        self.logger.log(
                            f"[{lineno}]",
                            f"定义标记: {line[1]} = {constants[line[1]]}"
                        )

                    else:
                        self.logger.log(
                            f"[{lineno}]",
                            "ERROR?",
                            "WARNING!!!",
                            "无匹配常量语法,",
                            "但是似乎此处应定义常量或标记!"
                        )
                else:
                    self.logger.log(
                        f"[{lineno}]",
                        "ERROR?",
                        "WARNING!!!",
                        "无匹配常量语法,",
                        "但是似乎此处应定义常量或标记!"
                    )
            else:
                self.logger.log(f"[{lineno}]", "无常量定义")
        self.logger.log("[CONST+MARK]", "常量解析完成")
        self.logger.log("[CONST+MARK]", f"常量数量: {len(constants)}")
        for i in constants:
            self.logger.log("[CHECKOUT][检出]", f"{i} = {constants[i]}")

        for line, lineno in zip(lines, range(len(lines))):
            s = 0

            self.logger.log(f"[{lineno}]", "正在解析指令")
            self.logger.log(f"[{lineno}]", "正在分割元素")
            for e, i in zip(line, range(len(line))):
                self.logger.log(f"[{lineno}][{i}]", f"正在匹配元素{{{e}}}")
                if self.ag[e]:
                    s += self.ag[e].code * self.ag[e].weight
                    self.logger.log(f"[{lineno}][{i}]", f"匹配到别名: {self.ag[e]}")

                elif re.match(r"0[bB][01]+|0[xX][a-fA-F0-9]+|\d+$", e):
                    s += int(e, 0)
                    self.logger.log(f"[{lineno}][{i}]", f"匹配到常数: {int(e, 0)}")

                elif e in constants:
                    s += constants[e]
                    self.logger.log(f"[{lineno}][{i}]", f"匹配到常量: {constants[e]}")

                else:
                    self.logger.log(f"[{lineno}][{i}]", "无匹配的汇编别名")
                    self.logger.log(
                        f"[{lineno}][{i}]",
                        "ERROR!!!",
                        "触发错误: 无匹配汇编别名错误",
                        "NoneMatchAliasNameError!!!"
                    )
                    self.logger.err(
                        "[ERROR] 触发错误: 无匹配汇编别名错误 {NoneMatchAliasNameError}",
                        "NoneMatchAliasNameError: 没有与之匹配的汇编别名!"
                        "NoneMatchAliasNameError: 请检查汇编别名组及其开发文档, 并修改汇编代码!",
                        "ERROR: 无法修复的错误, 代码解析失败, 即将退出编译, 编译终止!!!",
                        "CompilerError: By the NoneMatchAliasNameError, Compiler Stop!",
                        "Compilation Behavior Stop",
                        "You should know: COMPILER STOP!",
                        "COMPILER STOP!",
                        "EXIT WITH CODE: -1 AND 114514 WITHOUT 0 OR 666",
                    )

            ig.append(
                Instruct(
                    s >> 24 & 0xFF,
                    s >> 16 & 0xFF,
                    s >> 8 & 0xFF,
                    s & 0xFF
                )
            )
            self.logger.log(f"[{lineno}]", f"解析完成, 指令码 = {s}")
            self.logger.log(f"[{lineno}]: 生成指令:", ig[-1])

        return ig

    @staticmethod
    def decode(code: str) -> list[list[str]]:
        """
        将代码解码为列表, 每一个元素都是一行
        """
        code = re.sub(r"#.*$", "", code, flags=re.MULTILINE)
        code = re.sub(r"(\n*)([:,])(\n*)", r" ", code, flags=re.MULTILINE)
        return [re.split(r"\s+", line) for line in re.split(r"[;\n]", code) if line.strip()]

    @staticmethod
    def format(code: str) -> str:
        """
        美化代码, 使代码更符合标准规范, 但不会改动字符
        """
        code = code.strip()
        code = re.sub(r"(;)", r"\1\n", code, flags=re.MULTILINE)
        code = re.sub(r"(:)", r"\1\n", code, flags=re.MULTILINE)

        code = re.sub(r"\n+", "\n", code, flags=re.MULTILINE)
        code = re.sub(r" +", r" ", code, flags=re.MULTILINE)
        return code


if __name__ == '__main__':
    if os.path.exists(sys.argv[1]):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            with open(os.path.splitext(sys.argv[1])[0] + ".bin", "wb") as out:
                c = Compiler()
                for b in c.compile(f.read()).bin:
                    out.write(b)
