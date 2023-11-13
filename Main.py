#--*------------------ CanUseTimer Source Code ------------------*--#
#                                                                   #
# This is the source code of software CanUseTimer. You are          #
# free to edit and study based in GPLv3 License conduct,            #
# enjoy it. If you want to report a bug or help in the              #
# development of software visit our repository on Github.           #
#                                                                   #
# License:       GPLv3                                              #
# Creator:       Samuel de Oliveira (Samuel-de-Oliveira)            #
# Contribuitors: Francisco Lucas (LucasAlfare)                      #
# Repository:    https://gihub.com/Samuel-de-Oliveira/CanUseTimer   #
# Version:       0.2.2 BETA (unstable)                              #
#                                                                   #
#--*-------------------------------------------------------------*--#

# Import from the lib directory
from lib import *
from lib import __version__
from lib.winConf import *

# import libraries natives from the Python
from sys import argv
from time import sleep
import json

param = argv[1:]
sets = settings()

# Run main interface
if __name__ == "__main__":
    if len(param) == 0:
        # Starter window
        consoleClear()
        window('Welcome to CanUseTimer!', 'double_line')

        while True:
            # Menu list
            settings()
            line(style='double_line')
            print('Digit a one of these numbers:\033[36m')
            print("1: Start\n"
                "2: Settings\n"
                "3: Clear time list\n"
                "4: Credits\n"
                "5: Time list\n"
                "6: Remove time\n"
                "0: Exit\033[m")
            line(style='double_line')
            console = Console(size=6)

            consoleClear()

            # Timer
            if console == 1:
                window('Starting timer...')
                startTimer(sets.load['modality'])
            
            # Settings
            if console == 2:
                window('Settings')
                sets.manager()
                window('Settings\'s closed', 'double_line')
            
            # Clear time list
            if console == 3:
                if len(times.load[sets.load["modality"]]) >= 1:
                    times.load[sets.load["modality"]].clear()
                    window('The time list is cleared!', 'double_line')
                else:
                    window('The time list is empty...')
            
            # Credits
            if console == 4:
                window('Credits to:', 'double_line')
                print('The creator: Samuel de Oliveira(Github: Samuel-de-Oliveira) (All rights reserved).')
                print('Special thanks to contribuitors: Francisco Lucas(Github: LucasAlfare)')
                print(f'\nCanUseTimer\'s version: \033[33m{__version__}\033[m.\n'
                    'This software is a Open Source project to free use, study code and contributing,\n'
                    'for more info: https://github.com/Samuel-de-Oliveira/CanUseTimer.\n')
            
            # Time list
            if console == 5:
                window('Time list', 'double_line')
                timeList(sets.load['modality'])
                print(f'Average of 5: {timeFormat(showAverage(sets.load["modality"]))}')
            
            # Remove time
            if console == 6:
                window('Remove time')
                timeRemoval(sets.load['modality'])

            # Exit
            if console == 0:
                window("Bye bye!", "double_line")
                break

# --start parameter
elif param[0] in ('--start', '-s'):
    consoleClear()
    window('Start a Ao5!', 'double_line')
    for i in range(5):
        try: startTimer(param[1])
        except: startTimer(sets.load['modality'])
        sleep(0.6)

# --change-modality parameter
elif param[0] in ('--change-modality', '-C'):
    if param[1] in ('3x3', '2x2', '4x4', '5x5', '6x6', '7x7', 'pyra', 'skewb', 'sq1'):
        sets.load['modality'] = param[1]
        sets.Save()
    else: print('Sorry this modality doesn\'t exist.')

# --help parameter
elif param[0] in ('--help', '-h'):
    print('\nCanUseTimer Version: 0.2.1.2 BETA (Stable)\nThe command: canusetimer [--command] ...\n'
          '     the commands list:\n'
          '     --help or -h: Show help message (canusetimer -h).\n'
          '     --start or -s: Start a Avarage of 5 (canusetimer -s [modality]).\n'
          '     --change-modality or -C: Change the modality (canusetimer -C [modality])\n')

else: print('\n\033[31;1mUps... Maybe you digit something wrong!\033[m\ncommand "canusetimer -h" for help.\n')
