from time import sleep
from winConf import *

print('CanUseTimer Terminal\'s version: 0.1 BETA')

while True:
    sleep(0.3)
    line(style='doble_line')
    print("1: Start\n"
          "2: Change modality\n"
          "3: Exit")
    line(style='doble_line')

    console = int(input('>>: '))
    print()

    if console == 1: window('Start')
    if console == 2: window('Change modality')
    if console == 3: break
    print()

print('Bye, bye!')
