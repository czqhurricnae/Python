# -*- coding: utf-8 -*-
"""
    定制交互式命令行
    ~~~~~~~~~~~~

    交互式命令行可通过启动文件来配置, 当它启动时会查找环境变量PYTHONSTARUP,
    并且执行该变量中所指定文件里的程序代码. 有些Linux发型版本提供了一个默认
    的启动脚本, 它通常放在用户主目录下, 文件名是.pythonstartup. 按 Tab 键
    时自动补全内容和命令历史.
    基于readline模块实现的.

    :用法:
        1. 将该文件重命名为.pythonstartup, 并放置在用户主目录下.
        2. 将该文件链接到环境变量PYTHONSTARTUP, 例如在Bash和Korn Shell 使用的.profile文件中, 添加如下设置:
           export PYTHONSTARTUP=~/.pythonstartup
"""
import readline
import rlcompleter
import atexit
import os
# Tab completer
readline.parse_and_bind("tab: complete")
# History file
hisfile = os.path.join(os.environ["HOME"], ".pythonhistory")
try:
    readline.read_history_file(hisfile)
except IOError:
    pass
atexit.register(readline.write_history_file, hisfile)
del os, hisfile, readline, rlcompleter
