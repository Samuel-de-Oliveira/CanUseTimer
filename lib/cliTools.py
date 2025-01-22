### Here is the functions for CLI ###

# Imports
import os
import json
import time

# Windows import
if os.name in ('nt', 'dos'):
    import winsound
else: pass


# Class to be used only in this file
# to avoid circular imports
class readSettings():
    # Load file
    def __init__(self) -> None:
        if not os.name in ('nt', 'dos'):
            with open('setting.json', 'r') as f:
                config: str = f.read()
                self.load = json.loads(config)
        else:
            with open('setting.json', 'r') as f:
                config: str = f.read()
                self.load = json.loads(config)


# create a line
def line(size=40, style='basic') -> None:
    if style == 'basic': print('-' * size)
    elif style == 'double_line': print('=' * size)


# create the windown in top
def window(msg: str, style='basic') -> None:
    line(len(msg) + 10, style)
    print(f'|    {msg}    |')
    line(len(msg) + 10, style)


# Alert sound
def alert(intensity='low') -> None:
    # load settings
    sets = readSettings()

    if sets.load['sound']:
        # Windows
        if os.name in ('nt', 'dos'):
            if intensity == 'low':
                winsound.MessageBeep(type=winsound.MB_ICONEXCLAMATION)
            elif intensity == 'high':
                winsound.MessageBeep(type=winsound.MB_ICONHAND)

        # Linux and others
        else: print('\a', end='\a')

    else: pass


# Clear the comand line interface
def consoleClear() -> None:
    if os.name in ('nt', 'dos'): os.system('cls')
    else: os.system('clear')


# \r print
class rPrint():
    def __init__(self, msg: str) -> None:
        self.message: str = msg    
        self.msgSize: int = len(msg)
        print(msg, end='\r')
    

    def flush(self) -> None:
        print(
            ' ' * self.msgSize,
            end='\r'
        )


if __name__ == "__main__": print("Run the Main.py file to start program...")
