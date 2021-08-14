from lib import *
from winConf import *
from lib.Shufflers import *

print('CanUseTimer Terminal\'s version: 0.1.2.2 BETA.\n'
      'Created by: Samuel de Oliveira©.\n')
print('This software is open to free use and study code,\n'
      'for more info: github.com/samuel-de-oliveira/CanUseTimer-Terminal.\n')

modality = '3x3'

while True:
    line(style='double_line')
    print("1: Start\n"
          "2: Change modality\n"
          "3: Exit")
    line(style='double_line')

    console = Console(size=3).strip

    print()
    if console == 1:
        window('Starting timer...')
        startTimer(modality)
    if console == 2:
        window('Change modality')
        modality = defModality(modality)
    if console == 3:
        print('Bye, bye!')
        break
    print()
