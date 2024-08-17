## 运行法则

```shell
pip install prompt-toolkit
python ./IDEM-MoCPU/idem.py
```

## 构建法则之编译

```shell
pip install nuitka
nuitka --mingw64 --onefile --standalone --output-dir=.nuitka --show-progress --show-memory --windows-icon-from-ico=idem.ico idem.py
```

## 构建法则之打包

```shell
pip install pyinstaller
PyInstaller -F -i idem.ico idem.py
```
