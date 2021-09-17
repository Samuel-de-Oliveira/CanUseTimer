from lib import *
from winConf import *

consoleClear()
print('CanUseTimer Terminal\'s version: 0.1.4.1 BETA.\n'
      'This software is open to free use and study code,\n'
      'for more info: https://github.com/samuel-de-oliveira/CanUseTimer-Terminal.\n')
modality = '3x3'

while True:
    line(style='double_line')
    print('Digit a one of these numbers:')
    print("1: Start\n"
          "2: Change modality\n"
          "3: Credits\n"
          "4: Clear list\n"
          "5: Exit")
    line(style='double_line')
    console = Console(size=5)
    consoleClear()
    if console == 1:
        window('Starting timer...')
        startTimer(modality)
    if console == 2:
        window('Change modality')
        modality = defModality(modality)
    if console == 3:
        window('Credits to:', 'double_line')
        print('The creator: Samuel de Oliveira')
    if console == 4:
        timesSave.clear()
        window('The cube\'s times is cleared!')
    if console == 5: break
