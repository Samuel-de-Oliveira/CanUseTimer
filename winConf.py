# -*- Here is all the windows config from the program. -*- #
#     If you undestand what is here you can make your      #
#     window personal settings for program.                #

def line(size=40, style='basic') -> None:
    if style == 'basic': print('-' * size)
    elif style == 'double_line': print('=' * size)
    elif style == 'hashtag': print('#' * size)
    elif style == 'zigzag': print('W' * size)
    else: raise NameError(f'The style \'{style}\' doesn\'t exist.')

def window(msg='[Null]', style='basic') -> None:
    line(len(msg) + 10, style)
    print(f'|    {msg}    |')
    line(len(msg) + 10, style)

if __name__ == '__main__': print('You need to open: Main.py!')
