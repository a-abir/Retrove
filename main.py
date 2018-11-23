#!/usr/bin/env python3
import os

if os.name != 'nt':
    os.system('clear')
else:
    os.system('cls')

print(""" ____  ____  ____  ____   __   _  _  ____ """,
      """\n(  _ \(  __)(_  _)(  _ \ /  \ / )( \(  __)""",
      """\n )   / ) _)   )(   )   /(  O )\ \/ / ) _) """,
      """\n(__\_)(____) (__) (__\_) \__/  \__/ (____)""")


from game import *
if __name__ == '__main__':
    intro()
