def line(size=40, style='basic'):
    if style == 'basic': print('-' * size)
    elif style == 'double_line': print('=' * size)

def window(msg, style='basic'):
    line(len(msg) + 10, style)
    print(f'|    {msg}    |')
    line(len(msg) + 10, style)
