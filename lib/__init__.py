from winConf import window
from keyboard import is_pressed
from time import time, sleep
from lib.Shufflers import *
import os
import json

with open('lib/setting.json', 'r') as f: setting = json.loads(f.read())
timesSave = []

def consoleClear():
    if os.name in ('nt', 'dos'): os.system('cls')
    else: os.system('clear')

def Console(text='>>: ', size=2):
    while True:
        try:
            read = int(input(text))
            if 0 < read <= size: return read
            else: print(f'Digit a value in range of 1 to {size}')
        
        except KeyboardInterrupt: exit()
        except: print('Digit a valid value!')

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

def askP2():
    if setting['ask+2']: setting['ask+2'] = False
    else: setting['ask+2'] = True
    with open('lib/setting.json', 'w+') as f: f.write(json.dumps(setting, indent=True))
    window(f'ask +2 now is: {setting["ask+2"]}', 'double_line') 

def settingManager():
    while True:
        print('1: Change Modality\n'
              f'2: ask +2 >> {setting["ask+2"]}\n'
              '3: Close\n')
        numget = Console(size=3)

        consoleClear()
        if numget == 1:
            window('Change modality.')
            defModality(setting['modality'])
        if numget == 2: askP2()
        if numget == 3:
            window('Settings\'s closed', 'double_line')
            break

def defModality(modality):
    modals = ('3x3', '2x2', '4x4', '5x5', 'pyra', 'skewb')
    print('All modalities:', end='')
    for m in modals: print(f' {m}', end=' ')

    print()
    x = input('Digit the modality name: ')
    consoleClear()
    if x in modals:
        timesSave.clear()
        window('Modality changed!', 'double_line')
        setting['modality'] = x
        with open('lib/setting.json', 'w') as f: f.write(json.dumps(setting, indent=True))
        return x
    else:
        window('this modality doesn\'t exist.', 'double_line')
        return modality

def startTimer(modality):
    modalities = {'3x3': Salete('3x3'),
                  '2x2': Salete('2x2'),
                  '4x4': Lucia('4x4'),
                  '5x5': Lucia('5x5'),
                  'pyra': Cida('pyra'),
                  'skewb': Cida('skewb')}

    print(f'The actual modality is: {modality}\n'
          'Scrable: ', end='')
    for move in modalities[modality]: print(move ,end=' ')

    print('\nPress spacebar to start timer... (Press escape to exit)')
    while True:
        if is_pressed('space'):
            print('Continue pressing...')
            sleep(0.85)
            if is_pressed('space'):
                while is_pressed('space'): timer = time()
                while True:
                    totalTime = time() - timer
                    if is_pressed('space'): break
                    consoleClear()
                    if is_pressed('space'): break
                    window(f'\033[31m{timeFormat(totalTime)}\033[m')
                    if is_pressed('space'): break

                if setting['ask+2']:
                    consoleClear()
                    window(f'\033[32mTime: {timeFormat(totalTime)}\033[m')
                    plustwo = str(input('Is this a +2? [Y/n]')).replace(' ', '')
                    if plustwo in 'yY': totalTime = float(totalTime) + 2

                consoleClear()
                window(f'Time: {timeFormat(totalTime)}', 'double_line') 
                timesSave.append(totalTime)
                print('_-_-_-_-_-_- Times -_-_-_-_-_-_')
                for n, t in enumerate(timesSave): print(f'{n+1} - {timeFormat(t)}')
                print('_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')
                print(f'Average of 5: {timeFormat(showAverage())}')

                break
            else: print('The timer not start, you need press until 0.85secs.') 
        if is_pressed('escape'): consoleClear(); break

if __name__ == '__main__': print('You need to open: Main.py!')
