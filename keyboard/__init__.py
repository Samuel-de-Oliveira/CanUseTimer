from __future__ import print_function as _print_function

version = '0.13.5'

import re as _re
import itertools as _itertools
import collections as _collections
from threading import Thread as _Thread, Lock as _Lock
import time as _time
_time.monotonic = getattr(_time, 'monotonic', None) or _time.time

try:
    long, basestring
    _is_str = lambda x: isinstance(x, basestring)
    _is_number = lambda x: isinstance(x, (int, long))
    import Queue as _queue
    from threading import _Event as _UninterruptibleEvent
except NameError:
    _is_str = lambda x: isinstance(x, str)
    _is_number = lambda x: isinstance(x, int)
    import queue as _queue
    from threading import Event as _UninterruptibleEvent
_is_list = lambda x: isinstance(x, (list, tuple))

class _State(object): pass

class _Event(_UninterruptibleEvent):
    def wait(self):
        while True:
            if _UninterruptibleEvent.wait(self, 0.5): break

import platform as _platform
if _platform.system() == 'Windows': from. import _winkeyboard as _os_keyboard
elif _platform.system() == 'Linux': from. import _nixkeyboard as _os_keyboard
elif _platform.system() == 'Darwin': from. import _darwinkeyboard as _os_keyboard
else: raise OSError("Unsupported platform '{}'".format(_platform.system()))

from ._keyboard_event import KEY_DOWN, KEY_UP, KeyboardEvent
from ._generic import GenericListener as _GenericListener
from ._canonical_names import all_modifiers, sided_modifiers, normalize_name

_modifier_scan_codes = set()
def is_modifier(key):
    if _is_str(key): return key in all_modifiers
    else:
        if not _modifier_scan_codes:
            scan_codes = (key_to_scan_codes(name, False) for name in all_modifiers) 
            _modifier_scan_codes.update(*scan_codes)
        return key in _modifier_scan_codes
_pressed_events_lock = _Lock()
_pressed_events = {}
_physically_pressed_keys = _pressed_events
_logically_pressed_keys = {}
class _KeyboardListener(_GenericListener):
    transition_table = {
        ('free',       KEY_UP,   'modifier'): (False, True,  'free'),
        ('free',       KEY_DOWN, 'modifier'): (False, False, 'pending'),
        ('pending',    KEY_UP,   'modifier'): (True,  True,  'free'),
        ('pending',    KEY_DOWN, 'modifier'): (False, True,  'allowed'),
        ('suppressed', KEY_UP,   'modifier'): (False, False, 'free'),
        ('suppressed', KEY_DOWN, 'modifier'): (False, False, 'suppressed'),
        ('allowed',    KEY_UP,   'modifier'): (False, True,  'free'),
        ('allowed',    KEY_DOWN, 'modifier'): (False, True,  'allowed'),

        ('free',       KEY_UP,   'hotkey'):   (False, None,  'free'),
        ('free',       KEY_DOWN, 'hotkey'):   (False, None,  'free'),
        ('pending',    KEY_UP,   'hotkey'):   (False, None,  'suppressed'),
        ('pending',    KEY_DOWN, 'hotkey'):   (False, None,  'suppressed'),
        ('suppressed', KEY_UP,   'hotkey'):   (False, None,  'suppressed'),
        ('suppressed', KEY_DOWN, 'hotkey'):   (False, None,  'suppressed'),
        ('allowed',    KEY_UP,   'hotkey'):   (False, None,  'allowed'),
        ('allowed',    KEY_DOWN, 'hotkey'):   (False, None,  'allowed'),

        ('free',       KEY_UP,   'other'):    (False, True,  'free'),
        ('free',       KEY_DOWN, 'other'):    (False, True,  'free'),
        ('pending',    KEY_UP,   'other'):    (True,  True,  'allowed'),
        ('pending',    KEY_DOWN, 'other'):    (True,  True,  'allowed'),
        ('suppressed', KEY_UP,   'other'):    (False, False, 'allowed'),
        ('suppressed', KEY_DOWN, 'other'):    (True,  True,  'allowed'),
        ('allowed',    KEY_UP,   'other'):    (False, True,  'allowed'),
        ('allowed',    KEY_DOWN, 'other'):    (False, True,  'allowed'),
    }

    def init(self):
        _os_keyboard.init()
        self.active_modifiers = set()
        self.blocking_hooks = []
        self.blocking_keys = _collections.defaultdict(list)
        self.nonblocking_keys = _collections.defaultdict(list)
        self.blocking_hotkeys = _collections.defaultdict(list)
        self.nonblocking_hotkeys = _collections.defaultdict(list)
        self.filtered_modifiers = _collections.Counter()
        self.is_replaying = False
        self.modifier_states = {}

    def pre_process_event(self, event):
        for key_hook in self.nonblocking_keys[event.scan_code]: key_hook(event)
        with _pressed_events_lock: hotkey = tuple(sorted(_pressed_events))
        for callback in self.nonblocking_hotkeys[hotkey]: callback(event)
        return event.scan_code or (event.name and event.name != 'unknown')

    def direct_callback(self, event):
        if self.is_replaying: return True
        if not all(hook(event) for hook in self.blocking_hooks): return False
        event_type = event.event_type
        scan_code = event.scan_code

        with _pressed_events_lock:
            if event_type == KEY_DOWN:
                if is_modifier(scan_code): self.active_modifiers.add(scan_code)
                _pressed_events[scan_code] = event
            hotkey = tuple(sorted(_pressed_events))
            if event_type == KEY_UP:
                self.active_modifiers.discard(scan_code)
                if scan_code in _pressed_events: del _pressed_events[scan_code]

        for key_hook in self.blocking_keys[scan_code]:
            if not key_hook(event): return False
        accept = True

        if self.blocking_hotkeys:
            if self.filtered_modifiers[scan_code]:
                origin = 'modifier'
                modifiers_to_update = set([scan_code])
            else:
                modifiers_to_update = self.active_modifiers
                if is_modifier(scan_code):
                    modifiers_to_update = modifiers_to_update | {scan_code}
                callback_results = [callback(event) for callback in self.blocking_hotkeys[hotkey]]
                if callback_results:
                    accept = all(callback_results)
                    origin = 'hotkey'
                else: origin = 'other'

            for key in sorted(modifiers_to_update):
                transition_tuple = (self.modifier_states.get(key, 'free'), event_type, origin)
                should_press, new_accept, new_state = self.transition_table[transition_tuple]
                if should_press: press(key)
                if new_accept is not None: accept = new_accept
                self.modifier_states[key] = new_state

        if accept:
            if event_type == KEY_DOWN:_logically_pressed_keys[scan_code] = event
            elif event_type == KEY_UP and scan_code in _logically_pressed_keys: del _logically_pressed_keys[scan_code]
        self.queue.put(event)
        return accept

    def listen(self):_os_keyboard.listen(self.direct_callback)

_listener = _KeyboardListener()

def key_to_scan_codes(key, error_if_missing=True):
    if _is_number(key): return (key,)
    elif _is_list(key): return sum((key_to_scan_codes(i) for i in key), ())
    elif not _is_str(key): raise ValueError('Unexpected key type ' + str(type(key)) + ', value (' + repr(key) + ')')

    normalized = normalize_name(key)
    if normalized in sided_modifiers:
        left_scan_codes = key_to_scan_codes('left ' + normalized, False)
        right_scan_codes = key_to_scan_codes('right ' + normalized, False)
        return left_scan_codes + tuple(c for c in right_scan_codes if c not in left_scan_codes)

    try:
        t = tuple(_collections.OrderedDict((scan_code, True) for scan_code, modifier in _os_keyboard.map_name(normalized)))
        e = None
    except (KeyError, ValueError) as exception:
        t = ()
        e = exception

    if not t and error_if_missing: raise ValueError('Key {} is not mapped to any known key.'.format(repr(key)), e)
    else: return t

def parse_hotkey(hotkey):
    if _is_number(hotkey) or len(hotkey) == 1:
        scan_codes = key_to_scan_codes(hotkey)
        step = (scan_codes,)
        steps = (step,)
        return steps
    elif _is_list(hotkey):
        if not any(map(_is_list, hotkey)):
            step = tuple(key_to_scan_codes(k) for k in hotkey)
            steps = (step,)
            return steps
        return hotkey

    steps = []
    for step in _re.split(r',\s?', hotkey):
        keys = _re.split(r'\s?\+\s?', step)
        steps.append(tuple(key_to_scan_codes(key) for key in keys))
    return tuple(steps)

def send(hotkey, do_press=True, do_release=True):
    _listener.is_replaying = True

    parsed = parse_hotkey(hotkey)
    for step in parsed:
        if do_press:
            for scan_codes in step:
                _os_keyboard.press(scan_codes[0])

        if do_release:
            for scan_codes in reversed(step):
                _os_keyboard.release(scan_codes[0])

    _listener.is_replaying = False

press_and_release = send

def press(hotkey): send(hotkey, True, False)

def release(hotkey): send(hotkey, False, True)

def is_pressed(hotkey):
    _listener.start_if_necessary()

    if _is_number(hotkey):
        with _pressed_events_lock:
            return hotkey in _pressed_events

    steps = parse_hotkey(hotkey)
    if len(steps) > 1:
        raise ValueError("Impossible to check if multi-step hotkeys are pressed (`a+b` is ok, `a, b` isn't).")

    with _pressed_events_lock:
        pressed_scan_codes = set(_pressed_events)
    for scan_codes in steps[0]:
        if not any(scan_code in pressed_scan_codes for scan_code in scan_codes):
            return False
    return True

def call_later(fn, args=(), delay=0.001):
    thread = _Thread(target=lambda: (_time.sleep(delay), fn(*args)))
    thread.start()

_hooks = {}
def hook(callback, suppress=False, on_remove=lambda: None):
    if suppress:
        _listener.start_if_necessary()
        append, remove = _listener.blocking_hooks.append, _listener.blocking_hooks.remove
    else: append, remove = _listener.add_handler, _listener.remove_handler

    append(callback)
    def remove_():
        del _hooks[callback]
        del _hooks[remove_]
        remove(callback)
        on_remove()
    _hooks[callback] = _hooks[remove_] = remove_
    return remove_

def on_press(callback, suppress=False): return hook(lambda e: e.event_type == KEY_UP or callback(e), suppress=suppress)

def on_release(callback, suppress=False): return hook(lambda e: e.event_type == KEY_DOWN or callback(e), suppress=suppress)

def hook_key(key, callback, suppress=False):
    _listener.start_if_necessary()
    store = _listener.blocking_keys if suppress else _listener.nonblocking_keys
    scan_codes = key_to_scan_codes(key)
    for scan_code in scan_codes:
        store[scan_code].append(callback)

    def remove_():
        del _hooks[callback]
        del _hooks[key]
        del _hooks[remove_]
        for scan_code in scan_codes:
            store[scan_code].remove(callback)
    _hooks[callback] = _hooks[key] = _hooks[remove_] = remove_
    return remove_

def on_press_key(key, callback, suppress=False): return hook_key(key, lambda e: e.event_type == KEY_UP or callback(e), suppress=suppress)
def on_release_key(key, callback, suppress=False): return hook_key(key, lambda e: e.event_type == KEY_DOWN or callback(e), suppress=suppress)
def unhook(remove):_hooks[remove]()
unhook_key = unhook

def unhook_all():
    _listener.start_if_necessary()
    _listener.blocking_keys.clear()
    _listener.nonblocking_keys.clear()
    del _listener.blocking_hooks[:]
    del _listener.handlers[:]
    unhook_all_hotkeys()

def block_key(key):return hook_key(key, lambda e: False, suppress=True)
unblock_key = unhook_key

def remap_key(src, dst):
    def handler(event):
        if event.event_type == KEY_DOWN: press(dst)
        else: release(dst)
        return False
    return hook_key(src, handler, suppress=True)
unremap_key = unhook_key

def parse_hotkey_combinations(hotkey):
    def combine_step(step): return (tuple(sorted(scan_codes)) for scan_codes in _itertools.product(*step))
    return tuple(tuple(combine_step(step)) for step in parse_hotkey(hotkey))

def _add_hotkey_step(handler, combinations, suppress):
    container = _listener.blocking_hotkeys if suppress else _listener.nonblocking_hotkeys

    for scan_codes in combinations:
        for scan_code in scan_codes:
            if is_modifier(scan_code):
                _listener.filtered_modifiers[scan_code] += 1
        container[scan_codes].append(handler)

    def remove():
        for scan_codes in combinations:
            for scan_code in scan_codes:
                if is_modifier(scan_code):
                    _listener.filtered_modifiers[scan_code] -= 1
            container[scan_codes].remove(handler)
    return remove

_hotkeys = {}
def add_hotkey(hotkey, callback, args=(), suppress=False, timeout=1, trigger_on_release=False):
    if args:
        callback = lambda callback=callback: callback(*args)

    _listener.start_if_necessary()
    steps = parse_hotkey_combinations(hotkey)

    event_type = KEY_UP if trigger_on_release else KEY_DOWN
    if len(steps) == 1:
        handler = lambda e: (event_type == KEY_DOWN and e.event_type == KEY_UP and e.scan_code in _logically_pressed_keys) or (event_type == e.event_type and callback())
        remove_step = _add_hotkey_step(handler, steps[0], suppress)
        def remove_():
            remove_step()
            del _hotkeys[hotkey]
            del _hotkeys[remove_]
            del _hotkeys[callback]
        _hotkeys[hotkey] = _hotkeys[remove_] = _hotkeys[callback] = remove_
        return remove_

    state = _State()
    state.remove_catch_misses = None
    state.remove_last_step = None
    state.suppressed_events = []
    state.last_update = float('-inf')
    
    def catch_misses(event, force_fail=False):
        if (
                event.event_type == event_type
                and state.index
                and event.scan_code not in allowed_keys_by_step[state.index]
            ) or (
                timeout
                and _time.monotonic() - state.last_update >= timeout
            ) or force_fail:

            state.remove_last_step()

            for event in state.suppressed_events:
                if event.event_type == KEY_DOWN:press(event.scan_code)
                else:release(event.scan_code)
            del state.suppressed_events[:]

            index = 0
            set_index(0)
        return True

    def set_index(new_index):

        state.index = new_index
        if new_index == 0:state.remove_catch_misses = lambda: None
        elif new_index == 1:
            state.remove_catch_misses()
            state.remove_catch_misses = hook(catch_misses, suppress=True)

        if new_index == len(steps) - 1:
            def handler(event):
                if event.event_type == KEY_UP:
                    remove()
                    set_index(0)
                accept = event.event_type == event_type and callback() 
                if accept:
                    return catch_misses(event, force_fail=True)
                else:
                    state.suppressed_events[:] = [event]
                    return False
            remove = _add_hotkey_step(handler, steps[state.index], suppress)
        else:
            # Fix value of next_index.
            def handler(event, new_index=state.index+1):
                if event.event_type == KEY_UP:
                    remove()
                    set_index(new_index)
                state.suppressed_events.append(event)
                return False
            remove = _add_hotkey_step(handler, steps[state.index], suppress)
        state.remove_last_step = remove
        state.last_update = _time.monotonic()
        return False
    set_index(0)

    allowed_keys_by_step = [
        set().union(*step)
        for step in steps
    ]

    def remove_():
        state.remove_catch_misses()
        state.remove_last_step()
        del _hotkeys[hotkey]
        del _hotkeys[remove_]
        del _hotkeys[callback]
    _hotkeys[hotkey] = _hotkeys[remove_] = _hotkeys[callback] = remove_
    return remove_
register_hotkey = add_hotkey

def remove_hotkey(hotkey_or_callback):
    _hotkeys[hotkey_or_callback]()
unregister_hotkey = clear_hotkey = remove_hotkey

def unhook_all_hotkeys():
    _listener.blocking_hotkeys.clear()
    _listener.nonblocking_hotkeys.clear()
unregister_all_hotkeys = remove_all_hotkeys = clear_all_hotkeys = unhook_all_hotkeys

def remap_hotkey(src, dst, suppress=True, trigger_on_release=False):
    def handler():
        active_modifiers = sorted(modifier for modifier, state in _listener.modifier_states.items() if state == 'allowed')
        for modifier in active_modifiers:
            release(modifier)
        send(dst)
        for modifier in reversed(active_modifiers):
            press(modifier)
        return False
    return add_hotkey(src, handler, suppress=suppress, trigger_on_release=trigger_on_release)
unremap_hotkey = remove_hotkey

def stash_state():
    with _pressed_events_lock: state = sorted(_pressed_events)
    for scan_code in state: _os_keyboard.release(scan_code)

    return state

def restore_state(scan_codes):
    _listener.is_replaying = True

    with _pressed_events_lock:
        current = set(_pressed_events)
    target = set(scan_codes)
    for scan_code in current - target:
        _os_keyboard.release(scan_code)
    for scan_code in target - current:
        _os_keyboard.press(scan_code)

    _listener.is_replaying = False

def restore_modifiers(scan_codes): restore_state((scan_code for scan_code in scan_codes if is_modifier(scan_code)))

def write(text, delay=0, restore_state_after=True, exact=None):
    if exact is None:
        exact = _platform.system() == 'Windows'

    state = stash_state()
    
    if exact:
        for letter in text:
            if letter in '\n\b':
                send(letter)
            else:
                _os_keyboard.type_unicode(letter)
            if delay: _time.sleep(delay)
    else:
        for letter in text:
            try:
                entries = _os_keyboard.map_name(normalize_name(letter))
                scan_code, modifiers = next(iter(entries))
            except (KeyError, ValueError):
                _os_keyboard.type_unicode(letter)
                continue
            
            for modifier in modifiers:
                press(modifier)

            _os_keyboard.press(scan_code)
            _os_keyboard.release(scan_code)

            for modifier in modifiers:
                release(modifier)

            if delay:
                _time.sleep(delay)

    if restore_state_after:
        restore_modifiers(state)

def wait(hotkey=None, suppress=False, trigger_on_release=False):
    if hotkey:
        lock = _Event()
        remove = add_hotkey(hotkey, lambda: lock.set(), suppress=suppress, trigger_on_release=trigger_on_release)
        lock.wait()
        remove_hotkey(remove)
    else:
        while True:
            _time.sleep(1e6)

def get_hotkey_name(names=None):
    if names is None:
        _listener.start_if_necessary()
        with _pressed_events_lock:
            names = [e.name for e in _pressed_events.values()]
    else:
        names = [normalize_name(name) for name in names]
    clean_names = set(e.replace('left ', '').replace('right ', '').replace('+', 'plus') for e in names)
    modifiers = ['ctrl', 'alt', 'shift', 'windows']
    sorting_key = lambda k: (modifiers.index(k) if k in modifiers else 5, str(k))
    return '+'.join(sorted(clean_names, key=sorting_key))

def read_event(suppress=False):
    queue = _queue.Queue(maxsize=1)
    hooked = hook(queue.put, suppress=suppress)
    while True:
        event = queue.get()
        unhook(hooked)
        return event

def read_key(suppress=False):
    event = read_event(suppress)
    return event.name or event.scan_code

def read_hotkey(suppress=True):
    queue = _queue.Queue()
    fn = lambda e: queue.put(e) or e.event_type == KEY_DOWN
    hooked = hook(fn, suppress=suppress)
    while True:
        event = queue.get()
        if event.event_type == KEY_UP:
            unhook(hooked)
            with _pressed_events_lock:
                names = [e.name for e in _pressed_events.values()] + [event.name]
            return get_hotkey_name(names)

def get_typed_strings(events, allow_backspace=True):
    backspace_name = 'delete' if _platform.system() == 'Darwin' else 'backspace'

    shift_pressed = False
    capslock_pressed = False
    string = ''
    for event in events:
        name = event.name
        if event.name == 'space':
            name = ' '

        if 'shift' in event.name:
            shift_pressed = event.event_type == 'down'
        elif event.name == 'caps lock' and event.event_type == 'down':
            capslock_pressed = not capslock_pressed
        elif allow_backspace and event.name == backspace_name and event.event_type == 'down':
            string = string[:-1]
        elif event.event_type == 'down':
            if len(name) == 1:
                if shift_pressed ^ capslock_pressed:
                    name = name.upper()
                string = string + name
            else:
                yield string
                string = ''
    yield string

_recording = None
def start_recording(recorded_events_queue=None):
    recorded_events_queue = recorded_events_queue or _queue.Queue()
    global _recording
    _recording = (recorded_events_queue, hook(recorded_events_queue.put))
    return _recording

def stop_recording():
    global _recording
    if not _recording:
        raise ValueError('Must call "start_recording" before.')
    recorded_events_queue, hooked = _recording
    unhook(hooked)
    return list(recorded_events_queue.queue)

def record(until='escape', suppress=False, trigger_on_release=False):
    start_recording()
    wait(until, suppress=suppress, trigger_on_release=trigger_on_release)
    return stop_recording()

def play(events, speed_factor=1.0):
    state = stash_state()

    last_time = None
    for event in events:
        if speed_factor > 0 and last_time is not None:
            _time.sleep((event.time - last_time) / speed_factor)
        last_time = event.time

        key = event.scan_code or event.name
        press(key) if event.event_type == KEY_DOWN else release(key)

    restore_modifiers(state)
replay = play

_word_listeners = {}
def add_word_listener(word, callback, triggers=['space'], match_suffix=False, timeout=2):
    state = _State()
    state.current = ''
    state.time = -1

    def handler(event):
        name = event.name
        if event.event_type == KEY_UP or name in all_modifiers: return

        if timeout and event.time - state.time > timeout: state.current = ''
        state.time = event.time

        matched = state.current == word or (match_suffix and state.current.endswith(word))
        if name in triggers and matched:
            callback()
            state.current = ''
        elif len(name) > 1: state.current = ''
        else: state.current += name

    hooked = hook(handler)
    def remove():
        hooked()
        del _word_listeners[word]
        del _word_listeners[handler]
        del _word_listeners[remove]
    _word_listeners[word] = _word_listeners[handler] = _word_listeners[remove] = remove
    return remove

def remove_word_listener(word_or_handler): _word_listeners[word_or_handler]()

def add_abbreviation(source_text, replacement_text, match_suffix=False, timeout=2):
    replacement = '\b'*(len(source_text)+1) + replacement_text
    callback = lambda: write(replacement)
    return add_word_listener(source_text, callback, match_suffix=match_suffix, timeout=timeout)

register_word_listener = add_word_listener
register_abbreviation = add_abbreviation
remove_abbreviation = remove_word_listener
