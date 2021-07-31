def line(size=40, style='basic'):
    if style == 'basic':
        print('-' * size)

def window(msg='[Null]', style='basic'):
    line(len(msg)+6, style)
    print(f'|  {msg}  |')
    line(len(msg)+6, style)