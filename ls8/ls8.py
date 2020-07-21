#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

cpu = CPU()


#DAY 1---
#cpu.load('examples/print8.ls8')
#DAY 2---
cpu.load('examples/mult.ls8')
#DAY 3---
# cpu.load('examples/stack.ls8')
#DAY 4---
# cpu.load('examples/call.ls8')
#SPRINT

cpu.run()

