from lib import *
from winConf import *
import json

consoleClear()
print('CanUseTimer\'s version: 0.1.4.3 BETA.\n'
      'This software is open to free use and study code,\n'
      'for more info: https://github.com/samuel-de-oliveira/CanUseTimer.\n')

while True:
    with open('lib/setting.json', 'r') as f: setting = json.loads(f.read())
    line(style='double_line')
    print('Digit a one of these numbers:')
    print("1: Start\n"
          "2: Settings\n"
          "3: Clear list\n"
          "4: Credits\n"
          "5: Exit")
    line(style='double_line')
    console = Console(size=5)
    consoleClear()
    if console == 1: 
        window('Starting timer...')
        startTimer(setting['modality'])
    if console == 2 :
        window('Settings')
        settingManager()
    if console == 3:
        timesSave.clear() 
        window('The cube\'s times is cleared!', 'double_line')
    if console == 4:
        window('Credits to:', 'double_line')
        print('The creator: Samuel de Oliveira')
    if console == 5: break
