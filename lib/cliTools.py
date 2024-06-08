### Here is the window configuration ###
import os
# from . import settings

if os.name in ('nt', 'dos'):
    import winsound
else: pass

# sets = settings()

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
    # Windows
    if os.name in ('nt', 'dos'):
        if intensity == 'low':
            winsound.MessageBeep(type=winsound.MB_ICONEXCLAMATION)
        elif intensity == 'high':
            winsound.MessageBeep(type=winsound.MB_ICONHAND)

    # Linux and others
    else: print('\a', end='\a') 


# Clear the comand line interface
def consoleClear() -> None:
    if os.name in ('nt', 'dos'): os.system('cls')
    else: os.system('clear')


if __name__ == "__main__": print("Run the Main.py file to start program...")
