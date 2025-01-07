#--*------------------ CanUseTimer Source Code ------------------*--#
#                                                                   #
# This is the source code of software CanUseTimer. You are          #
# free to edit and study based in GPLv3 License conduct,            #
# enjoy it. If you want to report a bug or help in the              #
# development of software visit the software's repository           #
# on Github.                                                        #
#                                                                   #
# License:       GPLv3                                              #
# Creator:       Samuel de Oliveira (Samuel-de-Oliveira)            #
# Contribuitors: Francisco Lucas (LucasAlfare)                      #
# Repository:    https://gihub.com/Samuel-de-Oliveira/CanUseTimer   #
# Version:       0.2.3 BETA (Unstable)                              #
#                                                                   #
#--*-------------------------------------------------------------*--#

# Import from the lib directory
from lib import *
from lib import __version__
from lib.cliTools import *

# import libraries natives from the Python
from sys import argv
from time import sleep
import json

# Setting config
loadingMsg = rPrint("Please, wait everything be ready...")
param: list = argv[1:]
sets = settings()
update = UpdateManager()
loadingMsg.flush()

### -*- CanUseTimer Parameters -*- ###
if len(param) >= 1:

    # Counting the corrects parameters
    param_count: int = 0

    for i, p in enumerate(param):
        # --show parameter
        if p in ('--show', '-s'):
            param_count += 1
            window('Show the current time list', 'double_line')
            timeList(sets.load['modality'])
        
        # --change-modality parameter
        elif p in ('--change-modality', '-C'):
            param_count += 1
            if param[i + 1] in ('3x3', '2x2', '4x4', '5x5', '6x6', '7x7', 'pyra', 'skewb', 'sq1'):
                sets.load['modality']: str = param[1]
                sets.Save()
            else:
                alert()
                print('Sorry this modality doesn\'t exist.')

        # --help parameter
        elif p in ('--help', '-h', '-?'):
            param_count += 1
            print(f'CanUseTimer Version: \033[34;1m{__version__}\033[m\n\n\tUSAGE: \033[1mcanusetimer [--command] ...\033[m\n'
                   '\tthe commands list:\n'
                   '\t\t\033[32;1m--help or -h:\033[m Show help message (canusetimer -h).\n'
                   '\t\t\033[32;1m--show or -s:\033[m Show the current time list (canusetimer -s)\n'
                   '\t\t\033[32;1m--change-modality\033[m or -C: Change the modality (canusetimer -C [modality])\n')

    # if not find a correct parameter
    if param_count <= 0:
        alert(intensity='high')
        print('\033[31;1mOops... Maybe you digit something wrong!\033[m\n'
              'command \033[1m"canusetimer -h"\033[m for help.\n')
        exit()


### -*- Run main interface -*- ###
if __name__ == "__main__":
    if len(param) == 0:
        # Starter window
        update.verify()
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
                  "5: Show time list\n"
                  "6: Remove time\n"
                  "0: Exit\033[m")
            line(style='double_line')
            console: int = Console(size=6)

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
            
            # Show time list
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
                # Save all data
                window("Saving all data...")
                sets.Save()
                times.Save()
                consoleClear()

                # Finally it breaks the loop
                window("Bye bye!", "double_line")
                break
