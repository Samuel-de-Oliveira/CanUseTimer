#-----------*- CanUseTimer main modules -*-----------#
#                                                    # 
# This is the modules main library for CanUsetimer   #
# here you find all functions used in the Main.py    #
# file.                                              #
#                                                    #
#--*----------------------------------------------*--#

# Imports from the software lib 
from lib.cliTools import *
from lib.Shufflers import *

# Imports from other Python libraries
from keyboard import is_pressed
from time import time, sleep
import os
import json

# Version constant #
__version__ = "0.2.2.1 BETA (Unstable Release)"

# Time list saver class
class timesSaved():
    def __init__(self) -> None:
        if not os.path.exists("timesSaved.json"):
                with open('timesSaved.json', 'w') as f:
                    f.write(json.dumps(
                        {"3x3": [],
                         "2x2": [],
                         "4x4": [],
                         "5x5": [],
                         "6x6": [],
                         "7x7": [],
                         "pyra": [],
                         "skewb": [],
                         "sq1": []},
                         indent=True))
        else: pass

        with open('timesSaved.json', 'r') as f: self.load = json.loads(f.read())

    # Save time list
    def Save(self) -> None:
        with open('timesSaved.json', 'w+') as f:
            f.write(json.dumps(self.load,
                               indent=True))


# Init Time list
times = timesSaved()


# Settings class to configure software.
class settings():
    # Get informations in "setting.json" file
    def __init__(self) -> None:
        # If the system isn't Windows
        if not os.name in ('nt', 'dos'):
            # Check if the setting file exists
            if not os.path.exists("lib/setting.json"):
                with open('lib/setting.json', 'w') as f:
                    f.write(json.dumps({"modality": "3x3",
                                        "ask+2": True}, indent=True))
            else: pass

            with open('lib/setting.json', 'r') as f: self.load = json.loads(f.read())

        # Same process on Windows systems
        else:
            # Check if the setting file exists
            if not os.path.exists("setting.json"):
                with open('setting.json', 'w') as f:
                    f.write(json.dumps({"modality": "3x3",
                                        "ask+2": True}, indent=True))
            else: pass

            with open('setting.json', 'r') as f: self.load = json.loads(f.read())


    # Save informations in "setting.json" file
    def Save(self) -> None:
        if not os.name in ('nt', 'dos'): # Non-Windows systems
            with open('lib/setting.json', 'w') as f: f.write(json.dumps(self.load, indent=True))
        else: # Windows systems
            with open('setting.json', 'w') as f: f.write(json.dumps(self.load, indent=True))


    # Setting manager interface
    def manager(self) -> None:
        while True:
            try:
                line(style='double_line')
                print('\033[36m1: Change modality\n'
                     f'2: Ask +2 >> {self.load["ask+2"]}\n'
                     '3: Close\033[m')
                line(style='double_line')
                self.numget = Console(size=3)

                consoleClear()
                self.listWithFunctions = [
                    self.easterEgg, # Number 0
                    self.Modality, # Number 1
                    self.askP2, # Number 2
                ]

                if self.numget == 3: break
                else: self.listWithFunctions[self.numget]()

            # In case of a ctrl+C press
            except KeyboardInterrupt:
                consoleClear()
                break


    # Ask +2 configuration
    def askP2(self) -> None:
        self.load['ask+2'] = not self.load['ask+2']
        self.Save()
        window(f'ask +2 now is: {self.load["ask+2"]}', 'double_line')
        alert()


    # Modality configuration
    def Modality(self) -> str:
        window('Change modality')
        
        modality = self.load['modality']
        # Show current modalities
        modals = ('3x3', '2x2', '4x4', '5x5', '6x6', '7x7', 'pyra', 'skewb', 'sq1')
        print('All modalities:', end='')
        for m in modals:
            if modality == m: print('\033[34;1m', end='')
            else: print('\033[32m', end='')

            print(f' {m}', end=' ')
            print('\033[m', end='')

        # Break line
        print() 

        x = input('Digit the modality\'s name: ')
        consoleClear()

        # Selecting modality
        if x in modals:
            # Changing modality
            self.load['modality'] = x
            self.Save()

            window('Modality changed', 'double_line')
            alert()
            return x
        else:
            window('This modality doesn\'t exist', 'double_line')
            alert(intensity='high')
            return modality

    def sound(self) -> None: pass

    # Easter Egg
    def easterEgg(self) -> None:
        window('Oh no! zero maybe does not works... :P', 'double_line')
        alert()


# Remove a time
def timeRemoval(modality: str) -> None:
    if len(times.load[modality]) > 0:
        print('Digit the number of time you\'d like to remove: (Digit "0" to cancel)')
        timeList(modality)
        removeTime = Console(size=len(times.load[modality]))
        consoleClear()

        if removeTime == 0:
            window('you\'ve caceled this operation', "double_line")
        else:
            del times.load[modality][removeTime - 1]
            window("Time removed successfully!", "double_line")

    else: print('Is empty...')


# Console to get the user input
def Console(text='>>: ', size=2) -> int:
    while True:
        try:
            read = int(input(text))
            if 0 <= read <= size: return read
            else: print(f'\033[1;31mDigit a value in range of 1 to {size}\033[m')
        
        except KeyboardInterrupt: consoleClear(); alert(intensity='high'); exit()
        except: print('\033[1;31mPlease, Digit a valid number!\033[m')


# Convert seconds to minutes function
def timeFormat(time: float) -> str:
    if not time == None:
        if time < 60: return f'{time:.2f}'
        else:
            x = int(time // 60)
            y = time % 60

            if y < 10:
                y = '0' + f'{y:.2f}'
                return f'{x}:{y}' 
            else: return f'{x}:{y:.2f}'


# Ao5 function
def showAverage(modality: str) -> float:
    if len(times.load[modality]) >= 5:
        timesUse = 0
        for t in times.load[modality]: timesUse += float(t)
        timesUse -= float(max(times.load[modality]))
        timesUse -= float(min(times.load[modality]))
        timesUse /= len(times.load[modality]) - 2

        return float(f'{timesUse:.2f}')


# Time List
def timeList(modality: str) -> None:
    print(f'Current modality: \033[34;1m{modality}\033[m')
    print('_-_-_-_-_-_- Times -_-_-_-_-_-_')
    if len(times.load[modality]) <= 0: print('The list is empty...')
    else:
        for n, t in enumerate(times.load[modality]): print(f'\033[1m{n+1} - {timeFormat(t)}\033[m')
    print('_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')


# The timer function (This is important for the program! =^-^=)
def startTimer(modality: str) -> None:
    # To see the modalities shufflers check the file: Shufflers.py
    modalities = {'3x3': s3x3_shuffler('3x3'),
                  '2x2': s3x3_shuffler('2x2'),
                  '4x4': s4x4_shuffler('4x4'),
                  '5x5': s4x4_shuffler('5x5'),
                  '6x6': s6x6_shuffler('6x6'),
                  '7x7': s6x6_shuffler('7x7'),
                  'pyra': pyra_shuffler('pyra'),
                  'skewb': pyra_shuffler('skewb'),
                  'sq1': sq1_shuffler()}

    # Show shuffler
    print(f'The current modality is: {modality}\n'
          'Scrable: \033[1;34m', end='')
    for move in modalities[modality]: print(move ,end=' ')

    print('\033[m\nPress spacebar to start timer... (Press escape to exit)')

    while True:
        try:
            if is_pressed('space'):
                consoleClear()
                window('keep pressing...')
                sleep(0.85)
                if is_pressed('space'):
                    consoleClear()
                    window('Leave spacebar...')
                    while is_pressed('space'): timer = time()

                    # Timer working
                    while True:
                        totalTime = time() - timer
                        if is_pressed('space'): break
                        consoleClear()
                            
                        if is_pressed('space'): break
                        window(timeFormat(totalTime))

                        if is_pressed('space'): break

                    # Ask +2
                    if settings().load['ask+2']:
                        consoleClear()
                        alert()
                        window(f'Time: {timeFormat(totalTime)}')
                        plustwo = str(input('Is this a +2? [Y/n]')).replace(' ', '')
                        if plustwo in 'yY': totalTime = float(totalTime) + 2

                    # Time list
                    consoleClear()
                    window(f'Time: {timeFormat(totalTime)}', 'double_line')
                    times.load[modality].append(totalTime)
                    timeList(modality)
                    print(f'Average of 5: {timeFormat(showAverage(modality))}')

                    # End
                    break

                # In case you don't waited the cooldown
                else:
                    consoleClear()
                    window('The timer doesn\'t start, you need press until have 0.85 secondss.')
                
            # Exit Timer
            if is_pressed('escape'):
                consoleClear()
                alert(intensity='high')
                window('Timer\'s closed...', 'double_line')
                sleep(0.15)
                break

        except KeyboardInterrupt:
            consoleClear()
            alert(intensity='high')
            window('Timer\'s closed...', 'double_line')
            sleep(0.15)
            break


if __name__ == "__main__": print("Run the Main.py file to start the program...")
