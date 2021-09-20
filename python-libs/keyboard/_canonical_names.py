from __future__ import unicode_literals
try:basestring
except NameError:basestring = str
import _platform
canonical_names = {
    'escape': 'esc',
    'del': 'delete',
    'control': 'ctrl',

    'left arrow': 'left',
    'up arrow': 'up',
    'down arrow': 'down',
    'right arrow': 'right',

    'control': 'ctrl',

    'left control': 'left ctrl',
    'right control': 'right ctrl',

    "division": "÷",
    "dkshade": "▓",
    "dnblock": "▄",
    "dollar": "$",
    "dollarinferior": "",
    "dollaroldstyle": "",
    "dollarsuperior": "",
    "dong": "₫",
    "DongSign": "₫",
    "dot": ".",
    "dotaccent": "˙",
    "Dotaccentsmall": "",
    "dotbelowcomb": "̣",
    "dotlessi": "ı",
    "dotlessj": "",
    "dotmath": "⋅",
    "Dsmall": "",
    "dstroke": "đ",
    "Dstroke": "Đ",
    "dsuperior": "",
    "Eacute": "É",
    "eacute": "é",
    "Eacutesmall": "",
    "Ebreve": "Ĕ",
    "ebreve": "ĕ",
    }
sided_modifiers = {'ctrl', 'alt', 'shift', 'windows'}
all_modifiers = {'alt', 'alt gr', 'ctrl', 'shift', 'windows'} | set('left ' + n for n in sided_modifiers) | set('right ' + n for n in sided_modifiers)

if platform.system() == 'Darwin':
    canonical_names.update({
        "command": "command",
        "windows": "command",
        "cmd": "command",
        "win": "command",
        "backspace": "delete",
        'alt gr': 'alt' # Issue #117
    })
    all_modifiers = {'alt', 'ctrl', 'shift', 'windows'}
if platform.system() == 'Linux':
    canonical_names.update({
        "select": "end",
        "find": "home",
        'next': 'page down',
        'prior': 'page up',
    })

def normalize_name(name):
    if not name or not isinstance(name, basestring):
        raise ValueError('Can only normalize non-empty string names. Unexpected '+ repr(name))

    if len(name) > 1:
        name = name.lower()
    if name != '_' and '_' in name:
        name = name.replace('_', ' ')

    return canonical_names.get(name, name)
