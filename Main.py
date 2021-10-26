from lib import *
from winConf import *
import json
from sys import argv

param = argv[1:]
sets = settings()

if len(param) == 0:
    consoleClear()
    print('CanUseTimer\'s version: \033[33m0.2.1 BETA.\033[m\n'
          'This software is open to free use and study code,\n'
          'for more info: https://github.com/Samuel-de-Oliveira/CanUseTimer.\n')
    while True:
        settings()
        line(style='double_line')
        print('Digit a one of these numbers:\033[36m')
        print("1: Start\n"
              "2: Settings\n"
              "3: Clear list\n"
              "4: Credits\n"
              "5: Exit\033[m")
        line(style='double_line')
        console = Console(size=5)

        consoleClear()
        if console == 1:
            window('Starting timer...')
            startTimer(sets.load['modality'])
        if console == 2:
            window('Settings')
            sets.manager()
            window('Settings\'s closed', 'double_line')
        if console == 3:
            timesSave.clear()
            window('The time list is cleared!', 'double_line')
        if console == 4:
            window('Credits to:', 'double_line')
            print('The creator: Samuel de Oliveira (All rights reserved).')
        if console == 5: break

elif param[0] in ('--start', '-s'):
    consoleClear()
    window('Start a Ao5!', 'double_line')
    for i in range(5):
        try: startTimer(param[1])
        except: startTimer(sets.load['modality'])

elif param[0] in ('--change-modality', '-C'):
    if param[1] in ('3x3', '2x2', '4x4', '5x5', '6x6', '7x7', 'pyra', 'skewb'):
        sets.load['modality'] = param[1]
        sets.Save()
    else: print('Sorry this modality doesn\'t exist.')

elif param[0] in ('--help', '-h'):
    print('\nCanUseTimer Version: 0.2.1\nThe command: canusetimer [--command] ...\n'
          '     the commands list:\n'
          '     --help or -h: show help message (canusetimer --help).\n'
          '     --start or -s: start a Avarage of 5 (canusetimer -s [modality]).\n'
          '     --change-modality or -C: \n')
else: print('\n\033[31;1mUps... Maybe you digit something wrong!\033[m\nUse --help for help.\n')
