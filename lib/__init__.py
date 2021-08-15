from winConf import window
from keyboard import is_pressed
from time import time, sleep
from lib.Shufflers import *

modalities = {'3x3': Salete(size=20),
              '2x2': Salete(size=10),
              'pyra': Cida(size=8, corner=5)}

def Console(text='>>: ', size=2):
    while True:
        try:
            read = int(input(text))
            if 0 < read <= size: return read
            else: print(f'Digit a value in range of 1 to {size}')
        
        except KeyboardInterrupt: exit()
        except: print('Digit a valid value')

def defModality(modality):
    print('All modalities:', end='')
    for m in modalities.keys(): print(f' {m}', end=' ')

    print()
    x = input('Digit the modality name: ')

    if x in modalities.keys(): return x
    else:
        print('this modality doesn\'t exist')
        return modality

def startTimer(modality):
    print(f'The actual modality is: {modality}\n'
          f'Scrable: {modalities[modality]}')

    print('Press spacebar to start timer... (Press esc to exit)')
    while True:
        if is_pressed('space'):
            print('Continue pressing...')
            sleep(0.85)
            if is_pressed('space'):
                while is_pressed('space'): timer = time()

                print('Timer start...\n')
                while True:
                    if is_pressed('space'): break

                window(f'Time: {time() - timer:.2f}', 'double_line')
                break
            else: print('The timer not start, you need press until 0.85secs.')
        
        if is_pressed('escape'): break
    
if __name__ == '__main__': print('You need to open: main.py!')
