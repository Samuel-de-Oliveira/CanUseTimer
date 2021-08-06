from lib import *
from winConf import *
from lib.Shufflers import *

print('CanUseTimer Terminal\'s version: 0.1.1 BETA')

while True:
    line(style='double_line')
    print("1: Start\n"
          "2: Change modality\n"
          "3: Exit")
    line(style='double_line')

    console = Console(size=3)

    print()
    if console == 1:
        window('Starting timer...')
        startTimer()

    if console == 2:
        window('Change modality')
        defModality()

    if console == 3: break
    print()

print('Bye, bye!')
