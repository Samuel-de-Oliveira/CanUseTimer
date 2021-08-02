
from time import time, sleep

def Console(text='>>: ', size=2):
    while True:
        try:
            read = int(input(text))
            if 0 < read <= size: return read
            else: print(f'Digit a value in range of 1 to {size}')
        
        except KeyboardInterrupt: exit()
        except: print('Digit a valid value')

def startTimer(): print('Not done...')
    
if __name__ == '__main__': print('You need to open: main.py!')
