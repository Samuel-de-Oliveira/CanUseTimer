def line(size=40, style='basic'):
    if style == 'basic': print('-' * size)
    if style == 'doble_line': print('=' * size)
    if style == 'hashtag': print('#' * size)

def window(msg='[Null]', style='basic'):
    line(len(msg) + 10, style)
    print(f'|    {msg}    |')
    line(len(msg) + 10, style)
