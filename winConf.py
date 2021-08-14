def line(size=40, style='basic'):
    if style == 'basic': print('-' * size)
    if style == 'double_line': print('=' * size)
    if style == 'hashtag': print('#' * size)
    else: NameError

def window(msg='[Null]', style='basic'):
    line(len(msg) + 10, style)
    print(f'|    {msg}    |')
    line(len(msg) + 10, style)

if __name__ == '__main__': print('You need to open: main.py!')
