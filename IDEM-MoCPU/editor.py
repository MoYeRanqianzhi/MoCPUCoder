import difflib
import os
import re
import time
from datetime import datetime
from typing import Callable

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.formatted_text import StyleAndTextTuples
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.output import ColorDepth
from prompt_toolkit.shortcuts import radiolist_dialog, button_dialog, input_dialog, message_dialog, yes_no_dialog
from prompt_toolkit.styles import Style

from MoCPU import AliasType, AliasGroup, standard
from constant import *
from enums import *
from style import *


def generateMoCPUCompleter(ag: AliasGroup) -> Completer:
    # op = [a for a in ag if a.type is AliasType.OPCODE]
    # v1 = [a for a in ag if a.type is AliasType.VALUE1]
    # v2 = [a for a in ag if a.type is AliasType.VALUE2]
    # tar = [a for a in ag if a.type is AliasType.TARGET]
    # com = [a for a in ag if a.type is AliasType.COMPOSE]
    # const = [a for a in ag if a.type is AliasType.CONSTANT]
    # no = [a for a in ag if a.type is AliasType.NONE]
    #
    # nest = {}
    #
    # nest.update(
    #     {
    #         n.name: {
    #             o.name: None#{
                    # n.name: {
                    #     _1.name: {
                    #         n.name: {
                    #             _2.name: {
                    #                 n.name: {
                    #                     t.name: {
                    #                         n.name: {
                    #                             ct.name: {
                    #                                 n.name: None
                    #                             }
                    #                         },
                    #                         ct.name: {
                    #                             n.name: None
                    #                         }
                    #                     }
                    #                 },
                    #                 t.name: {
                    #                     n.name: {
                    #                         ct.name: {
                    #                             n.name: None
                    #                         }
                    #                     },
                    #                     ct.name: {
                    #                         n.name: None
                    #                     }
                    #                 }
                    #             }
                    #         },
                    #         _2.name: {
                    #             n.name: {
                    #                 t.name: {
                    #                     n.name: {
                    #                         ct.name: {
                    #                             n.name: None
                    #                         }
                    #                     },
                    #                     ct.name: {
                    #                         n.name: None
                    #                     }
                    #                 }
                    #             },
                    #             t.name: {
                    #                 n.name: {
                    #                     ct.name: {
                    #                         n.name: None
                    #                     }
                    #                 },
                    #                 ct.name: {
                    #                     n.name: None
                    #                 }
                    #             }
                    #         }
                    #     }
                    # },
                    # _1.name: {
                    #     n.name: {
                    #         _2.name: {
                    #             n.name: {
                    #                 t.name: {
                    #                     n.name: {
                    #                         ct.name: {
                    #                             n.name: None
                    #                         }
                    #                     },
                    #                     ct.name: {
                    #                         n.name: None
                    #                     }
                    #                 }
                    #             },
                    #             t.name: {
                    #                 n.name: {
                    #                     ct.name: {
                    #                         n.name: None
                    #                     }
                    #                 },
                    #                 ct.name: {
                    #                     n.name: None
                    #                 }
                    #             }
                    #         }
                    #     },
                    #     _2.name: {
                    #         n.name: {
                    #             t.name: {
                    #                 n.name: {
                    #                     ct.name: {
                    #                         n.name: None
                    #                     }
                    #                 },
                    #                 ct.name: {
                    #                     n.name: None
                    #                 }
                    #             }
                    #         },
                    #         t.name: {
                    #             n.name: {
                    #                 ct.name: {
                    #                     n.name: None
                    #                 }
                    #             },
                    #             ct.name: {
                    #                 n.name: None
                    #             }
                    #         }
                    #     }
                    # }
                # }
    #         }
    #         for o in op
    #         # for _1 in v1
    #         # for _2 in v2
    #         # for t in tar
    #         # for c in com
    #         # for ct in const
    #         for n in no
    #     }
    # )

    # nest.update(
    #     {
    #         o.name: {
    #             n.name: {
    #                 _1.name: {
    #                     n.name: {
    #                         _2.name: {
    #                             n.name: {
    #                                 t.name: {
    #                                     n.name: {
    #                                         ct.name: {
    #                                             n.name: None
    #                                         }
    #                                     },
    #                                     ct.name: {
    #                                         n.name: None
    #                                     }
    #                                 }
    #                             },
    #                             t.name: {
    #                                 n.name: {
    #                                     ct.name: {
    #                                         n.name: None
    #                                     }
    #                                 },
    #                                 ct.name: {
    #                                     n.name: None
    #                                 }
    #                             }
    #                         }
    #                     },
    #                     _2.name: {
    #                         n.name: {
    #                             t.name: {
    #                                 n.name: {
    #                                     ct.name: {
    #                                         n.name: None
    #                                     }
    #                                 },
    #                                 ct.name: {
    #                                     n.name: None
    #                                 }
    #                             }
    #                         },
    #                         t.name: {
    #                             n.name: {
    #                                 ct.name: {
    #                                     n.name: None
    #                                 }
    #                             },
    #                             ct.name: {
    #                                 n.name: None
    #                             }
    #                         }
    #                     }
    #                 }
    #             },
    #             _1.name: {
    #                 n.name: {
    #                     _2.name: {
    #                         n.name: {
    #                             t.name: {
    #                                 n.name: {
    #                                     ct.name: {
    #                                         n.name: None
    #                                     }
    #                                 },
    #                                 ct.name: {
    #                                     n.name: None
    #                                 }
    #                             }
    #                         },
    #                         t.name: {
    #                             n.name: {
    #                                 ct.name: {
    #                                     n.name: None
    #                                 }
    #                             },
    #                             ct.name: {
    #                                 n.name: None
    #                             }
    #                         }
    #                     }
    #                 },
    #                 _2.name: {
    #                     n.name: {
    #                         t.name: {
    #                             n.name: {
    #                                 ct.name: {
    #                                     n.name: None
    #                                 }
    #                             },
    #                             ct.name: {
    #                                 n.name: None
    #                             }
    #                         }
    #                     },
    #                     t.name: {
    #                         n.name: {
    #                             ct.name: {
    #                                 n.name: None
    #                             }
    #                         },
    #                         ct.name: {
    #                             n.name: None
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #         for o in op
    #         for _1 in v1
    #         for _2 in v2
    #         for t in tar
    #         for c in com
    #         for ct in const
    #         for n in no
    #     }
    # )
    #
    # nest.update(
    #     {
    #         ct.name: {
    #             ct.name: {
    #                 ct.name: {
    #                     ct.name: {
    #                         ct.name: {
    #                             ct.name: None
    #                         }
    #                     }
    #                 }
    #             }
    #         }
    #         for ct in const
    #     }
    # )
    #
    # nest.update(
    #     {
    #         c.name: {
    #             n.name: {
    #                 _1.name: {
    #                     n.name: {
    #                         _2.name: {
    #                             n.name: {
    #                                 t.name: {
    #                                     n.name: None,
    #                                 }
    #                             },
    #                             t.name: {
    #                                 n.name: None,
    #                             }
    #                         }
    #                     },
    #                     _2.name: {
    #                         n.name: {
    #                             t.name: {
    #                                 n.name: None,
    #                             }
    #                         },
    #                         t.name: {
    #                             n.name: None,
    #                         }
    #                     }
    #                 }
    #             },
    #             _1.name: {
    #                 n.name: {
    #                     _2.name: {
    #                         n.name: {
    #                             t.name: {
    #                                 n.name: None,
    #                             }
    #                         },
    #                         t.name: {
    #                             n.name: None,
    #                         }
    #                     }
    #                 },
    #                 _2.name: {
    #                     n.name: {
    #                         t.name: {
    #                             n.name: None,
    #                         }
    #                     },
    #                     t.name: {
    #                         n.name: None,
    #                     }
    #                 }
    #             },
    #             _2.name: {
    #                 n.name: {
    #                     t.name: {
    #                         n.name: None,
    #                     }
    #                 },
    #                 t.name: {
    #                     n.name: None,
    #                 }
    #             },
    #             t.name: {
    #                 n.name: None,
    #             }
    #         }
    #         for _1 in v1
    #         for _2 in v2
    #         for t in tar
    #         for c in com
    #         for n in no
    #     }
    # )

    # return NestedCompleter.from_nested_dict(nest)

    return WordCompleter(["const", "CONST", "mark", "MARK"] + [a.name for a in ag])


class IDEM:
    def __init__(
            self,
            file="",
            ag: AliasGroup = standard
    ):
        self.file = file
        self.savedCode = ""

        self.ag = ag

        self.history = InMemoryHistory()

        self.style = Style(
            editorSidebarStyle
            + editorCompletionMenuStyle
            + dialogStyle
            + editorCodeHighlightStyle
        )

        self.completer = generateMoCPUCompleter(self.ag)
        self.keybindings = KeyBindings()

        self.session = PromptSession(
            message=self.SideBar,
            prompt_continuation=self.SideBar,
            multiline=True,
            wrap_lines=False,
            history=self.history,
            lexer=self,
            style=self.style,
            color_depth=ColorDepth.TRUE_COLOR,
            auto_suggest=AutoSuggestFromHistory(),
            completer=self.completer,
            complete_in_thread=True,
            enable_history_search=False,
            mouse_support=True,
            input_processors=[],
            key_bindings=self.keybindings,
            editing_mode=EditingMode.VI,
            vi_mode=True,
        )
        self.__binds__()

    async def __call__(self, default=None):
        if default is None:
            default = default_code

        return await self.session.prompt_async(default=default)

    def __binds__(self):
        # nothing
        self.keybindings.add(Keys.ControlC)(self.__nothing__)
        self.keybindings.add(Keys.Escape, Keys.Enter)(self.__nothing__)

        # quit
        self.keybindings.add(Keys.Escape, Keys.ControlQ)(self.quit)
        self.keybindings.add(Keys.Escape, Keys.ControlQ)(self.quit)
        self.keybindings.add(Keys.Escape, Keys.Escape, Keys.ControlQ, Keys.Enter)(self.quit)
        self.keybindings.add(Keys.Escape, Keys.Escape, Keys.ControlQ, Keys.Enter)(self.quit)
        self.keybindings.add(Keys.Escape, *"quit")(self.quit)
        self.keybindings.add(Keys.Escape, *"QUIT")(self.quit)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"quit", Keys.Enter, *"quit", )(self.quit)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"QUIT", Keys.Enter)(self.quit)

        # exit
        self.keybindings.add(Keys.ControlE)(self.exit)
        self.keybindings.add(Keys.Escape, *"exit")(self.exit)
        self.keybindings.add(Keys.Escape, *"EXIT")(self.exit)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"exit", Keys.Enter)(self.exit)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"EXIT", Keys.Enter)(self.exit)

        # key bindings help
        self.keybindings.add(Keys.ControlK)(self.keyBindingsHelp)

        # menu
        self.keybindings.add(Keys.ControlP)(self.menu)
        self.keybindings.add(Keys.Escape, *"menu")(self.menu)
        self.keybindings.add(Keys.Escape, *"MENU")(self.menu)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"menu", Keys.Enter)(self.menu)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"MENU", Keys.Enter)(self.menu)

        # undo
        self.keybindings.add(Keys.ControlZ)(self.undo)
        self.keybindings.add(Keys.Escape, *"undo")(self.undo)
        self.keybindings.add(Keys.Escape, *"UNDO")(self.undo)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"undo", Keys.Enter)(self.undo)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"UNDO", Keys.Enter)(self.undo)

        # comment
        self.keybindings.add(Keys.Escape, "/")(self.comment)
        self.keybindings.add(Keys.Escape, *"comment")(self.comment)
        self.keybindings.add(Keys.Escape, *"COMMENT")(self.comment)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"comment", Keys.Enter)(self.comment)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"COMMENT", Keys.Enter)(self.comment)

        # indent tab
        self.keybindings.add(Keys.BackTab)(self.indentTab)
        self.keybindings.add(Keys.Escape, *"indent")(self.indentTab)
        self.keybindings.add(Keys.Escape, *"INDENT")(self.indentTab)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"indent", Keys.Enter)(self.indentTab)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"INDENT", Keys.Enter)(self.indentTab)

        # open file
        self.keybindings.add(Keys.Escape, *"openfile")(self.openFile)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"openfile", Keys.Enter)(self.openFile)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"OPENFILE", Keys.Enter)(self.openFile)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"file", *"openfile", Keys.Enter)(self.openFile)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"FILE", *"openfile", Keys.Enter)(self.openFile)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"file", *"OPENFILE", Keys.Enter)(self.openFile)
        self.keybindings.add(Keys.Escape, Keys.Escape, *"FILE", *"OPENFILE", Keys.Enter)(self.openFile)

    def SideBar(self, width=0, line=0, is_soft_wrap=0):
        return self.LineNumberBar(line + 1)

    def RightLineNumberBar(self, line=1):
        return [
            ("class:side", " "),
            (
                "class:side.error"
                if line in self.errors
                else (
                    "class:side.constant"
                    if line in self.constants
                    else (
                        "class:side.mark"
                        if line in self.marks
                        else "class:side"
                    )
                ),
                "❱" if line in self.errors or line in self.constants or line in self.marks else " "
            ),
            ("class:side", " "),
        ]

    def LineNumberBar(self, line=1):
        return (
                self.RightLineNumberBar(line) +
                [
                    (
                        "class:side.line_number.current"
                        if line == self.row + 1
                        else "class:side.line_number.disabled",
                        str(line).rjust(
                            len(
                                str(
                                    len(
                                        self.text.splitlines()
                                    )
                                )
                            )
                        )
                    ),
                    ("class:side", "  "),
                    ("class:side.separation", "│"),
                ]
        )

    @property
    def text(self):
        return self.document.text

    @property
    def row(self):
        return self.document.cursor_position_row

    @property
    def col(self):
        return self.document.cursor_position_col

    @property
    def document(self):
        return self.buffer.document

    @property
    def selection(self):
        return range(
            self.document.translate_index_to_position(self.buffer.document.selection_range()[0])[0],
            self.document.translate_index_to_position(self.buffer.document.selection_range()[1])[0] + 1
        )

    @property
    def buffer(self):
        return self.app.current_buffer

    @property
    def app(self):
        return self.session.app

    @staticmethod
    def __nothing__(*args):
        pass

    def quit(self, event=None):
        try:
            with open(f"idem.__{time.time()}__.record.code", "w", encoding="utf-8") as f:
                f.write(self.text)
        except Exception as e:
            with open(f"idem.__{time.time()}__.record.error", "w", encoding="utf-8") as f:
                f.write(str(e))
        finally:
            os._exit(0)

    async def exit(self, event=None):
        await self.finish()

    async def finish(self):
        if await yes_no_dialog(
                title="EXIT",
                text="是否确定退出IDEM?\nAre you sure to exit IDEM?",
                yes_text="Yes",
                no_text="NO",
                style=self.style
        ).run_async():
            if not self.checkSave():
                await self.save(code=self.text)
            self.clear()

    def clear(self):
        self.buffer.text = ""
        self.file = None
        self.app.exit()

    def checkSave(self):
        return self.text == self.savedCode

    async def save(self, event=None, file=None, code=None):
        if file is None:
            file = self.file
        if code is None:
            code = self.text
        if file:
            if not os.path.exists(os.path.dirname(file)):
                os.makedirs(os.path.dirname(file))
            with open(file, 'w', encoding="utf-8") as f:
                f.write(code)
        else:
            await self.saveAs(event=event, code=code)

    async def saveAs(self, event=None, code=None):
        if code is None:
            code = self.text

        path = ""
        while not path:
            path = await self.getPath()
            if path is None:
                return None

        if not os.path.isfile(path):
            path = os.path.join(path, await self.getFileName())

        self.file = path
        await self.save(event=event, file=path, code=code)

    def keyBindingsHelp(self, event=None):
        pass

    def menu(self, event=None):
        self.app.current_buffer.insert_text("Menu")

    def undo(self, event=None):
        self.buffer.undo()

    def comment(self, event=None):
        lines = self.buffer.text.split("\n")
        move = 0
        if self.buffer.selection_state is not None:
            if all([lines[line].lstrip()[0] == "#" for line in self.selection if lines[line].lstrip()]):
                for line in self.selection:
                    space_num_left = len(lines[line]) - len(lines[line].lstrip())
                    lines[line] = lines[line].lstrip()[1:]
                    space_num_right = len(lines[line]) - len(lines[line].lstrip())
                    num = ((space_num_left + space_num_right) // 4) * 4
                    lines[line] = " " * num + lines[line]
                    move -= space_num_left + space_num_right - num
            else:
                for line in self.selection:
                    num = len(lines[line]) - len(lines[line].lstrip())
                    lines[line] = " " * num + "# " + lines[line].lstrip()
                    move += 2
        else:
            if lines[self.row]:
                if lines[self.row].lstrip()[0] == "#":
                    space_num_left = len(lines[self.row]) - len(lines[self.row].lstrip())
                    lines[self.row] = lines[self.row].lstrip()[1:]
                    space_num_right = len(lines[self.row]) - len(lines[self.row].lstrip())
                    num = ((space_num_left + space_num_right) // 4) * 4
                    lines[self.row] = " " * num + lines[self.row]
                    move -= space_num_left + space_num_right - num
                else:
                    num = len(lines[self.row]) - len(lines[self.row].lstrip())
                    lines[self.row] = " " * num + "# " + lines[self.row].lstrip()
                    move += 2
            else:
                lines[self.row] = "# "
                move += 2

        self.buffer.text = "\n".join(lines)
        self.buffer.cursor_position += move

    def indentTab(self, event=None):
        lines = self.buffer.text.split("\n")
        move = 0
        if self.buffer.selection_state is not None:
            for line in self.selection:
                num = 4 - (len(lines[line]) - len(lines[line].lstrip())) % 4
                lines[line] = " " * num + lines[line]
                move += num
        else:
            num = 4 - (len(lines[self.row]) - len(lines[self.row].lstrip())) % 4
            lines[self.row] = " " * num + lines[self.row]
            move += num
        self.buffer.text = "\n".join(lines)
        self.buffer.cursor_position += move

    async def openFile(self, event=None):
        path = await self.getPath()
        if path is not None:
            if os.path.exists(path) and os.path.isfile(path):
                self.file = path
                self.app.exit()

    async def getPath(
            self,
            title="获取路径",
            text="请选择获取路径的途径",
            input_title="输入路径",
            input_text="请输入路径位置",
            choose_title="选择路径",
            choose_text="请选择路径位置",
    ):
        method = await button_dialog(
            title=title,
            text=text,
            buttons=[
                ("输入", GetPathMethod.Input),
                ("选择", GetPathMethod.Choose),
            ],
            style=self.style
        ).run_async()
        if method is GetPathMethod.Input:
            return await input_dialog(
                title=input_title,
                text=input_text,
                style=self.style
            ).run_async()
        elif method is GetPathMethod.Choose:
            return await self.getPathChooser()
        else:
            await message_dialog(
                title="ERROR",
                text="未知的选项",
                style=self.style
            ).run_async()

    async def getPathChooser(
            self,
            path=".",
            title="选择路径",
            text="请选择路径位置",
            option_title="操作",
            option_text="请选择操作",
    ):
        path = os.path.abspath(path)

        choose = await radiolist_dialog(
            title=title,
            text=text,
            values=[
                       (os.path.abspath(os.path.join(path, "..")), "...")
                   ] + [
                       (os.path.join(path, item), item) for item in os.listdir(path)
                   ],
            style=self.style
        ).run_async()

        if choose is not None:
            if os.path.isdir(choose):
                option = await radiolist_dialog(
                    title=option_title,
                    text=option_text,
                    values=[
                        (ChoosePathMethod.Into, "进入该文件夹"),
                        (ChoosePathMethod.Choose, "选择该文件夹")
                    ],
                    style=self.style
                ).run_async()
            else:
                option = await radiolist_dialog(
                    title=option_title,
                    text=option_text,
                    values=[
                        (ChoosePathMethod.Choose, "选择该文件")
                    ],
                    style=self.style
                ).run_async()

            if option is ChoosePathMethod.Into:
                return await self.getPathChooser(
                    path=choose,
                    title=title,
                    text=text,
                    option_title=option_title,
                    option_text=option_text
                )
            elif option is ChoosePathMethod.Choose:
                return choose
            else:
                return None
        else:
            return None

    async def getFileName(
            self,
            title="文件名",
            text="请输入文件名称，请注意带上拓展名(后缀)",
    ):
        name = ""
        while not name:
            name = await input_dialog(
                title=title,
                text=text,
                style=self.style
            ).run_async()
        return name

    def backup(self):
        diff = difflib.Differ()
        with open("_backup.idem.code", "w+", encoding="utf-8") as backup:
            _old = ""
            while True:
                _new = self.text
                if _new and not _old == _new:
                    backup.write("-" * 8 + str(datetime.now()) + "-" * 8 + "\n")
                    backup.write(_new + "\n")
                    backup.write("* -- Diff -- *\n")

                    different = list(diff.compare(_old.split("\n"), _new.split("\n")))
                    length = len(max(different, key=len))
                    backup.write("╭" + "─" * 3 + "┬" + "─" * length + "╮\n")
                    for i in different:
                        backup.write("│ " + i[0] + " │" + i[1:].ljust(length) + "│\n")
                    backup.write("╰" + "─" * 3 + "┴" + "─" * length + "╯\n")
                    _old = _new

                    backup.flush()
                    time.sleep(1)

    errors = set()

    marks = set()
    constants = set()

    markValues = {}
    constantValues = {}

    def checkConstantsAndMarks(self):
        marks = set()
        constants = set()

        markValues = {}
        constantValues = {}
        for line, num in zip(self.text.splitlines(), range(len(self.text.splitlines()))):
            for block in re.split(r"[;:,]\s*", line):
                if re.match(r"(\s*)(const|CONST)(\s*)([a-zA-Z_]\w*)(\s*)(=)(\s*)(0[bB][01]+|0[xX][a-fA-F0-9]+|\d+)(\s*)(.*)", block):
                    matched = re.match(r"(\s*)(const|CONST)(\s*)([a-zA-Z_]\w*)(\s*)(=)(\s*)(0[bB][01]+|0[xX][a-fA-F0-9]+|\d+)(\s*)(.*)", block)
                    if self.ag[matched[4]] is None and matched[4] not in ["const", "CONST", "mark", "MARK"]:
                        constants.add(num + 1)
                        constantValues.update(
                            {matched[4]: int(matched[8], 0)}
                        )
                elif re.match(r"(\s*)(mark|MARK)(\s*)([a-zA-Z_]\w*)(\s*)(.*)", block):
                    matched = re.match(r"(\s*)(mark|MARK)(\s*)([a-zA-Z_]\w*)(\s*)(.*)", block)
                    if self.ag[matched[4]] is None and matched[4] not in ["const", "CONST", "mark", "MARK"]:
                        marks.add(num + 1)
                        markValues.update(
                            {matched[4]: num + 1}
                        )
        self.marks = marks
        self.constants = constants
        self.markValues = markValues
        self.constantValues = constantValues

    def lex_block(self, document: Document, lineno: int, block: str):
        if re.match(r"(\s*)(const|CONST)(\s*)([a-zA-Z_]\w*)(\s*)(=)(\s*)(0[bB][01]+|0[xX][a-fA-F0-9]+|\d+)(\s*)(.*)", block):
            matched = re.match(r"(\s*)(const|CONST)(\s*)([a-zA-Z_]\w*)(\s*)(=)(\s*)(0[bB][01]+|0[xX][a-fA-F0-9]+|\d+)(\s*)(.*)", block)
            if self.ag[matched[4]] is not None or matched[4] in ["const", "CONST", "mark", "MARK"]:
                self.errors.add(lineno + 1)
                return [
                    ("class:mo", matched[1]),
                    ("class:mo.keyword", matched[2]),
                    ("class:mo", matched[3]),
                    ("class:mo.error", matched[4]),
                    ("class:mo", matched[5]),
                    ("class:mo", matched[6]),
                    ("class:mo", matched[7]),
                    ("class:mo.literal", matched[8]),
                    ("class:mo", matched[9]),
                    ("class:mo.error", matched[10])
                ]

            if matched[10]:
                self.errors.add(lineno + 1)

            return [
                ("class:mo", matched[1]),
                ("class:mo.keyword", matched[2]),
                ("class:mo", matched[3]),
                ("class:mo.name.constant", matched[4]),
                ("class:mo", matched[5]),
                ("class:mo", matched[6]),
                ("class:mo", matched[7]),
                ("class:mo.literal", matched[8]),
                ("class:mo", matched[9]),
                ("class:mo.error", matched[10])
            ]

        elif re.match(r"(\s*)(mark|MARK)(\s*)([a-zA-Z_]\w*)(\s*)(.*)", block):
            matched = re.match(r"(\s*)(mark|MARK)(\s*)([a-zA-Z_]\w*)(\s*)(.*)", block)
            if self.ag[matched[4]] is not None:
                self.errors.add(lineno + 1)
                return [
                    ("class:mo", matched[1]),
                    ("class:mo.keyword", matched[2]),
                    ("class:mo", matched[3]),
                    ("class:mo.error", matched[4]),
                    ("class:mo", matched[5]),
                    ("class:mo.error", matched[6])
                ]

            if matched[6]:
                self.errors.add(lineno + 1)

            return [
                ("class:mo", matched[1]),
                ("class:mo.keyword", matched[2]),
                ("class:mo", matched[3]),
                ("class:mo.name", matched[4]),
                ("class:mo", matched[5]),
                ("class:mo.error", matched[6])
            ]

        else:
            result = []
            for element, split in zip(
                    re.split(r"\s+", block),
                    re.findall(r"\s+", block) + [""]
            ):
                if not element:
                    pass

                elif re.match(r"\d+|0[bB][01]+|0[xX][a-fA-F0-9]+$", element):
                    result += [("class:mo.literal", element)]

                elif self.ag[element] is not None:
                    if self.ag[element].type is AliasType.OPCODE:
                        result += [("class:mo.opcode", element)]

                    if self.ag[element].type is AliasType.VALUE1:
                        result += [("class:mo.value1", element)]

                    if self.ag[element].type is AliasType.VALUE2:
                        result += [("class:mo.value2", element)]

                    if self.ag[element].type is AliasType.TARGET:
                        result += [("class:mo.target", element)]

                    if self.ag[element].type is AliasType.COMPOSE:
                        result += [("class:mo.builtin", element)]

                    if self.ag[element].type is AliasType.CONSTANT:
                        result += [("class:mo.function", element)]

                    if self.ag[element].type is AliasType.NONE:
                        result += [("class:mo.keyword", element)]

                elif element in ["const", "CONST", "mark", "MARK"]:
                    result += [("class:mo.keyword", element)]

                elif element in self.constantValues:
                    result += [("class:mo", element), ("class:mo.comment", f"[{self.constantValues[element]}]")]

                elif element in self.markValues:
                    result += [("class:mo", element), ("class:mo.comment", f"[{self.markValues[element]}]")]

                else:
                    self.errors.add(lineno + 1)
                    result += [("class:mo.error", element)]

                result += [("class:mo", split)]

            return result

    def lex_document(self, document: Document) -> Callable[[int], StyleAndTextTuples]:
        def lexer(lineno: int) -> StyleAndTextTuples:
            try:
                # 清理当前行的标记
                self.errors.remove(lineno + 1) if lineno + 1 in self.errors else None

                self.checkConstantsAndMarks()

                if not document.lines[lineno].strip():
                    return [("class:mo", document.lines[lineno])]
                else:
                    result = []

                    for block, split in zip(
                            re.split(
                                r"[;:,]\s*",  # 注: ":"冒号在汇编中无意义, 但是";"分号等同于换行符
                                re.sub(r"#.*$", "", document.lines[lineno])
                            ),
                            re.findall(
                                r"[;:,]\s*",
                                re.sub(r"#.*$", "", document.lines[lineno])
                            ) + [""]
                    ):
                        result += self.lex_block(document, lineno, block)
                        result += [("class:mo", split)]

                    if re.findall(r"#.*$", document.lines[lineno]):
                        for comment in re.findall(r"#.*$", document.lines[lineno]):
                            result += [("class:mo.comment", comment)]

                    return result
            except IndexError:
                return []

        return lexer


if __name__ == '__main__':
    m = IDEM()

    while True:
        os.system("cls")

        m()
