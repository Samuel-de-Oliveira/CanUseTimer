from lib import *
from winConf import *

consoleClear()
print('CanUseTimer Terminal\'s version: 0.1.3.2 BETA.\n'
      'Created by: Samuel de Oliveira©.\n')
print('This software is open to free use and study code,\n'
      'for more info: https://github.com/samuel-de-oliveira/CanUseTimer-Terminal.\n')

modality = '3x3'

while True:

    line(style='double_line')
    print('Digit one of these numbers and press return...')
    print("1: Start\n"
          "2: Change modality\n"
          "3: Credits\n"
          "4: Exit")
    line(style='double_line')

    console = Console(size=4)

    print()
    if console == 1:
        consoleClear()
        window('Starting timer...')
        startTimer(modality)
    if console == 2:
        consoleClear()
        window('Change modality')
        modality = defModality(modality)
    if console == 3:
        consoleClear()
        window('Credits to:', 'double_line')
        line()
        print('The creator: Samuel de Oliveira')
        line()
    if console == 4:
        consoleClear()
        break
    print()
