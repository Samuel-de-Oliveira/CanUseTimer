from time import sleep
from winConf import *

print('CanUseTimer Terminal\'s version BETA')

while True:
    sleep(0.4)
    line()
    print("1: \033[0;30;47mStart\n"
          "2: Change modality\n"
          "3: Exit"
          )
    line()
    console = int(input('>>: '))

    if console == 1: window('Start')
    if console == 2: window('Change modality')
    if console == 3: break

print('Bye, bye!')
