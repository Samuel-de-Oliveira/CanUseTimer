from winConf import window
from keyboard import is_pressed
from time import time
from lib.Shufflers import *

showModality = '3X3 cube'

def Console(text='>>: ', size=2):
    while True:
        try:
            read = int(input(text))
            if 0 < read <= size: return read
            else: print(f'Digit a value in range of 1 to {size}')
        
        except KeyboardInterrupt: exit()
        except: print('Digit a valid value')

def startTimer():
    print(f'The actual modality is: {showModality}\n',
          f'Scrable: {Salete(20)}')

    print('Press spacebar to start timer...')
    while True:
        if is_pressed('space'):

            print('Continue pressing...')
            while is_pressed('space'): timer = time()

            print('Timer start...\n')
            while True:
                if is_pressed('space'): break

            window(f'Time: {time() - timer:.2f}', 'double_line')
            break
    
if __name__ == '__main__': print('You need to open: main.py!')
