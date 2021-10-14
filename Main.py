from lib import *
from winConf import *
import json
from sys import argv

param = argv[1:]
consoleClear()
settings()

if len(param) == 0:
    print('CanUseTimer\'s version: 0.2 BETA.\n'
          'This software is open to free use and study code,\n'
          'for more info: https://github.com/samuel-de-oliveira/CanUseTimer.\n')
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
            startTimer(settings.load['modality'])
        if console == 2:
            window('Settings')
            settings.manager('')
        if console == 3:
            timesSave.clear()
            window('The cube\'s times is cleared!', 'double_line')
        if console == 4:
            window('Credits to:', 'double_line')
            print('The creator: Samuel de Oliveira')
        if console == 5: break

elif param[0] in ('--change-modality', '-c'):
    try:
        print(param[1])
        if param[1] in ('3x3', '2x2', '4x4', '5x5', 'pyra', 'skewb'):
            settings.load['modality'] = argv[2]
            with open('lib/setting.json', 'w+') as f: f.write(json.dump(settings.load))
        else: print('Digit a valid modality!')

    except: print('digit: canusetimer -c [modality name]')

elif param[0] in ('--start', '-s'): startTimer(settings.load['modality'])
