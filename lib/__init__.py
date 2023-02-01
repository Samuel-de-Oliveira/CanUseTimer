from lib.winConf import *
from keyboard import is_pressed
from time import time, sleep
from lib.Shufflers import *
import os, json

class settings():
    def __init__(self) -> None:
        if not os.name in ('nt', 'dos'):
            with open('lib/setting.json', 'r') as f: self.load = json.loads(f.read())
        else:
            with open('setting.json', 'r') as f: self.load = json.loads(f.read())

    def Save(self) -> None:
        if not os.name in ('nt', 'dos'):
            with open('lib/setting.json', 'w') as f: f.write(json.dumps(self.load, indent=True))
        else:
            with open('setting.json', 'w') as f: f.write(json.dumps(self.load, indent=True))

    def manager(self) -> None:
        while True:
            line(style='double_line')
            print('\033[36m1: Change modality\n'
                 f'2: Ask +2 >> {self.load["ask+2"]}\n'
                  '3: Close\033[m')
            line(style='double_line')
            numget = Console(size=3)

            consoleClear()
            if numget == 1: self.Modality(self.load['modality'])
            if numget == 2: self.askP2()
            if numget == 3: break

    def askP2(self) -> None:
        self.load['ask+2'] = not self.load['ask+2']
        self.Save()
        window(f'ask +2 now is: {self.load["ask+2"]}', 'double_line')

    def Modality(self, modality) -> str:
        window('Change modality')

        modals = ('3x3', '2x2', '4x4', '5x5', '6x6', '7x7', 'pyra', 'skewb', 'sq1')
        print('All modalities:', end='')
        for m in modals: print(f' {m}', end=' ')

        print() 
        x = input('Digit the modality\'s name: ')
        consoleClear()
        if x in modals:
            timesSave.clear()
            window('Modality changed', 'double_line')
            self.load['modality'] = x
            self.Save()
            return x
        else:
            window('This modality doesn\'t exist', 'double_line')
            return modality
 
timesSave = []

def consoleClear():
    if os.name in ('nt', 'dos'): os.system('cls')
    else: os.system('clear')

def Console(text='>>: ', size=2):
    while True:
        try:
            read = int(input(text))
            if 0 <= read <= size: return read
            else: print(f'\033[1;31mDigit a value in range of 1 to {size}\033[m')
        
        except KeyboardInterrupt: consoleClear(); exit()
        except: print('\033[1;31mPlease, Digit a valid number!\033[m')

def timeFormat(time):
    if not time == None:
        if time < 60: return f'{time:.2f}'
        else:
            x = int(time // 60)
            y = time % 60

            if y < 10:
                y = '0' + f'{y:.2f}'
                return f'{x}:{y}' 
            else: return f'{x}:{y:.2f}'

def showAverage():
    if len(timesSave) >= 5:
        timesUse = 0
        for t in timesSave: timesUse += float(t)
        timesUse -= float(max(timesSave))
        timesUse -= float(min(timesSave))
        timesUse /= len(timesSave) - 2

        return float(f'{timesUse:.2f}')

def timeList():
    print('_-_-_-_-_-_- Times -_-_-_-_-_-_')
    if len(timesSave) <= 0: print('The list is empty...')
    else:
        for n, t in enumerate(timesSave): print(f'\033[1m{n+1} - {timeFormat(t)}\033[m')
    print('_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')

def startTimer(modality):
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

                    while True:
                        totalTime = time() - timer
                        if is_pressed('space'): break
                        consoleClear()
                        if is_pressed('space'): break
                        window(timeFormat(totalTime))

                    if settings().load['ask+2']:
                        consoleClear()
                        window(f'Time: {timeFormat(totalTime)}')
                        plustwo = str(input('Is this a +2? [Y/n]')).replace(' ', '')
                        if plustwo in 'yY': totalTime = float(totalTime) + 2

                    consoleClear()
                    window(f'Time: {timeFormat(totalTime)}', 'double_line') 
                    timesSave.append(totalTime)
                    timeList()
                    print(f'Average of 5: {timeFormat(showAverage())}')

                    break
                else:
                    consoleClear()
                    window('The timer doesn\'t start, you need press until have 0.85secs.')
                
            if is_pressed('escape'):
                consoleClear()
                window('Timer\'s closed...', 'double_line')
                break

        except KeyboardInterrupt:
            consoleClear()
            window('Timer\'s closed...', 'double_line')
            break

if __name__ == "__main__": print("Run the Main.py file to start the program...")
