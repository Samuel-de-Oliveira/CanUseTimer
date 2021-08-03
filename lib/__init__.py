from keyboard import is_pressed
from time import time

def Console(text='>>: ', size=2):
    while True:
        try:
            read = int(input(text))
            if 0 < read <= size: return read
            else: print(f'Digit a value in range of 1 to {size}')
        
        except KeyboardInterrupt: exit()
        except: print('Digit a valid value')

def startTimer():
    print('Press spacebar to start timer...')
    while True:
        if is_pressed('space'):

            print('Continue pressing...')
            while is_pressed('space'): timer = time()

            print('Timer start...')
            while True:
                if is_pressed('space'): break

            print(f'Time: {time() - timer:.2f}')
            break
    
if __name__ == '__main__': print('You need to open: main.py!')
