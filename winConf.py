# To edit borders you need to edit settings.json file.

def line(size=40, style='basic'):
    if style == 'basic': print('-' * size)
    elif style == 'double_line': print('=' * size)
    elif style == 'hashtag': print('#' * size)
    elif style == 'zigzag': print('W' * size)
    else: raise NameError(f'The style \'{style}\' doesn\'t exist.')

def window(msg='[Null]', style='basic'):
    line(len(msg) + 10, style)
    print(f'|    {msg}    |')
    line(len(msg) + 10, style)

if __name__ == '__main__': print('You need to open: Main.py!')
