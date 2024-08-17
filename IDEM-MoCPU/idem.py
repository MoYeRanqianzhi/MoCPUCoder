import sys
import os
import asyncio
from threading import Thread
from editor import IDEM


async def main():
    os.system("title IDEM")

    file = ""
    if len(sys.argv) > 1:
        file = os.path.abspath(sys.argv[1])

    m = IDEM(file)
    Thread(
        target=m.backup,
        daemon=True
    ).start()
    while m.file is not None:
        code = None

        if m.file:
            code = ""
            if os.path.exists(m.file):
                with open(m.file, "r", encoding='utf-8') as f:
                    code = f.read()
        await m(code)


if __name__ == '__main__':
    asyncio.run(main())
    sys.exit(0)
