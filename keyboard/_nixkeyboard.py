import struct
import traceback
from time import time as now
from collections import namedtuple
from ._keyboard_event import KeyboardEvent, KEY_DOWN, KEY_UP
from ._canonical_names import all_modifiers, normalize_name
from ._nixcommon import EV_KEY, aggregate_devices, ensure_root

def cleanup_key(name):
    name = name.lstrip('+')
    is_keypad = name.startswith('KP_')
    for mod in ('Meta_', 'Control_', 'dead_', 'KP_'):
        if name.startswith(mod): name = name[len(mod):]

    if name == 'Remove': name = 'Delete'
    elif name == 'Delete': name = 'Backspace'

    if name.endswith('_r'): name = 'right ' + name[:-2]
    if name.endswith('_l'):name = 'left ' + name[:-2]

    return normalize_name(name), is_keypad

def cleanup_modifier(modifier):
    modifier = normalize_name(modifier)
    if modifier in all_modifiers: return modifier
    if modifier[:-1] in all_modifiers: return modifier[:-1]
    raise ValueError('Unknown modifier {}'.format(modifier))

from subprocess import check_output
from collections import defaultdict
import re

to_name = defaultdict(list)
from_name = defaultdict(list)
keypad_scan_codes = set()

def register_key(key_and_modifiers, name):
    if name not in to_name[key_and_modifiers]: to_name[key_and_modifiers].append(name)
    if key_and_modifiers not in from_name[name]: from_name[name].append(key_and_modifiers)

def build_tables():
    if to_name and from_name: return
    ensure_root()

    modifiers_bits = {
        'shift': 1,
        'alt gr': 2,
        'ctrl': 4,
        'alt': 8,
    }
    keycode_template = r'^keycode\s+(\d+)\s+=(.*?)$'
    dump = check_output(['dumpkeys', '--keys-only'], universal_newlines=True)
    for str_scan_code, str_names in re.findall(keycode_template, dump, re.MULTILINE):
        scan_code = int(str_scan_code)
        for i, str_name in enumerate(str_names.strip().split()):
            modifiers = tuple(sorted(modifier for modifier, bit in modifiers_bits.items() if i & bit))
            name, is_keypad = cleanup_key(str_name)
            register_key((scan_code, modifiers), name)
            if is_keypad:
                keypad_scan_codes.add(scan_code)
                register_key((scan_code, modifiers), 'keypad ' + name)

    if (125, ()) not in to_name or to_name[(125, ())] == 'alt':
        register_key((125, ()), 'windows')
    if (126, ()) not in to_name or to_name[(126, ())] == 'alt':
        register_key((126, ()), 'windows')

    if (127, ()) not in to_name:
        register_key((127, ()), 'menu')

    synonyms_template = r'^(\S+)\s+for (.+)$'
    dump = check_output(['dumpkeys', '--long-info'], universal_newlines=True)
    for synonym_str, original_str in re.findall(synonyms_template, dump, re.MULTILINE):
        synonym, _ = cleanup_key(synonym_str)
        original, _ = cleanup_key(original_str)
        if synonym != original:
            from_name[original].extend(from_name[synonym])
            from_name[synonym].extend(from_name[original])

device = None
def build_device():
    global device
    if device: return
    ensure_root()
    device = aggregate_devices('kbd')

def init():
    build_device()
    build_tables()

pressed_modifiers = set()

def listen(callback):
    build_device()
    build_tables()

    while True:
        time, type, code, value, device_id = device.read_event()
        if type != EV_KEY: continue

        scan_code = code
        event_type = KEY_DOWN if value else KEY_UP # 0 = UP, 1 = DOWN, 2 = HOLD

        pressed_modifiers_tuple = tuple(sorted(pressed_modifiers))
        names = to_name[(scan_code, pressed_modifiers_tuple)] or to_name[(scan_code, ())] or ['unknown']
        name = names[0]
            
        if name in all_modifiers:
            if event_type == KEY_DOWN:
                pressed_modifiers.add(name)
            else:
                pressed_modifiers.discard(name)

        is_keypad = scan_code in keypad_scan_codes
        callback(KeyboardEvent(event_type=event_type, scan_code=scan_code, name=name, time=time, device=device_id, is_keypad=is_keypad, modifiers=pressed_modifiers_tuple))

def write_event(scan_code, is_down):
    build_device()
    device.write_event(EV_KEY, scan_code, int(is_down))

def map_name(name):
    build_tables()
    for entry in from_name[name]: yield entry

    parts = name.split(' ', 1)
    if len(parts) > 1 and parts[0] in ('left', 'right'):
        for entry in from_name[parts[1]]: yield entry

def press(scan_code): write_event(scan_code, True)
def release(scan_code): write_event(scan_code, False)

def type_unicode(character):
    codepoint = ord(character)
    hexadecimal = hex(codepoint)[len('0x'):]

    for key in ['ctrl', 'shift', 'u']:
        scan_code, _ = next(map_name(key))
        press(scan_code)

    for key in hexadecimal:
        scan_code, _ = next(map_name(key))
        press(scan_code)
        release(scan_code)

    for key in ['ctrl', 'shift', 'u']:
        scan_code, _ = next(map_name(key))
        release(scan_code)

if __name__ == '__main__':
    def p(e): print(e)
    listen(p)
