from winConf import window
from keyboard import is_pressed
from time import time, sleep
from lib.Shufflers import *
import os

modalities = {'3x3': Salete(size=20),
              '2x2': Salete(size=10),
              'pyra': Cida(size=9, corner=4)}

timesSave = []

def consoleClear() -> None:
    if os.name in ('nt', 'dos'): os.system('cls')
    else: os.system('clear')

def Console(text='>>: ', size=2) -> int:
    while True:
        try:
            read = int(input(text))
            if 0 < read <= size: return read
            else: print(f'Digit a value in range of 1 to {size}')
        
        except KeyboardInterrupt: exit()
        except: print('Digit a valid value')

def timeFormat(time):
    
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
        timesUse /= 3

        return f'{timesUse:.2f}'

def defModality(modality) -> str:
    print('All modalities:', end='')
    for m in modalities.keys(): print(f' {m}', end=' ')

    print()
    x = input('Digit the modality name: ')

    if x in modalities.keys():
        consoleClear()
        window('Modality changed!')
        return x
    else:
        consoleClear()
        window('this modality doesn\'t exist.')
        return modality

def startTimer(modality) -> None:
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
                try:
                    while True:
                        totalTime = time() - timer
                        if is_pressed('space'): break
                        consoleClear()
                        window(timeFormat(totalTime), 'double_line')
                    consoleClear()
                    window(f'Time: {timeFormat(totalTime)}', 'double_line')
                    

                except KeyboardInterrupt: window('Timer Aborted!')
                except: window('Oops, something gone wrong')
                
                timesSave.append(timeFormat(totalTime))
                print('_-_-_-_-_-_- Times -_-_-_-_-_-_')
                for n, t in enumerate(timesSave): print(f'{n+1} - {t}')
                print('_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_')

                print(f'Average: {showAverage()}')

                break
            else: print('The timer not start, you need press until 0.85secs.')
        
        if is_pressed('escape'): consoleClear(); break

if __name__ == '__main__': print('You need to open: Main.py!')
