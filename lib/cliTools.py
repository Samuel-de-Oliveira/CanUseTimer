### Here is the window configuration ###
import os

if os.name in ('nt', 'dos'):
    import winsound


def line(size=40, style='basic'):
    if style == 'basic': print('-' * size)
    elif style == 'double_line': print('=' * size)


def window(msg, style='basic'):
    line(len(msg) + 10, style)
    print(f'|    {msg}    |')
    line(len(msg) + 10, style)


# Alert sound
def alert():
    if os.name in ('nt', 'dos'): print('\a', end='\a')
    else: print('\a', end='\a') 


# Clear the comand line interface
def consoleClear():
    if os.name in ('nt', 'dos'): os.system('cls')
    else: os.system('clear')


if __name__ == "__main__": print("Run the Main.py file to start program...")
