import ctypes
import ctypes.util
import Quartz
import time
import os
import threading
from AppKit import NSEvent
from ._keyboard_event import KeyboardEvent, KEY_DOWN, KEY_UP
from ._canonical_names import normalize_name

try: unichr
except NameError: unichr = chr

Carbon = ctypes.cdll.LoadLibrary(ctypes.util.find_library('Carbon'))

class KeyMap(object):
    non_layout_keys = dict((vk, normalize_name(name)) for vk, name in {
        0x24: 'return',
        0x30: 'tab',
        0x31: 'space',
        0x33: 'delete',
        0x35: 'escape',
        0x37: 'command',
        0x38: 'shift',
        0x39: 'capslock',
        0x3a: 'option',
        0x3b: 'control',
        0x3c: 'right shift',
        0x3d: 'right option',
        0x3e: 'right control',
        0x3f: 'function',
        0x40: 'f17',
        0x48: 'volume up',
        0x49: 'volume down',
        0x4a: 'mute',
        0x4f: 'f18',
        0x50: 'f19',
        0x5a: 'f20',
        0x60: 'f5',
        0x61: 'f6',
        0x62: 'f7',
        0x63: 'f3',
        0x64: 'f8',
        0x65: 'f9',
        0x67: 'f11',
        0x69: 'f13',
        0x6a: 'f16',
        0x6b: 'f14',
        0x6d: 'f10',
        0x6f: 'f12',
        0x71: 'f15',
        0x72: 'help',
        0x73: 'home',
        0x74: 'page up',
        0x75: 'forward delete',
        0x76: 'f4',
        0x77: 'end',
        0x78: 'f2',
        0x79: 'page down',
        0x7a: 'f1',
        0x7b: 'left',
        0x7c: 'right',
        0x7d: 'down',
        0x7e: 'up',
    }.items())
    layout_specific_keys = {}
    def __init__(self):
        CFTypeRef = ctypes.c_void_p
        CFDataRef = ctypes.c_void_p
        CFIndex = ctypes.c_uint64
        OptionBits = ctypes.c_uint32
        UniCharCount = ctypes.c_uint8
        UniChar = ctypes.c_uint16
        UniChar4 = UniChar * 4

        class CFRange(ctypes.Structure):
            _fields_ = [('loc', CFIndex),
                        ('len', CFIndex)]

        kTISPropertyUnicodeKeyLayoutData = ctypes.c_void_p.in_dll(Carbon, 'kTISPropertyUnicodeKeyLayoutData')
        shiftKey = 0x0200
        alphaKey = 0x0400
        optionKey = 0x0800
        controlKey = 0x1000
        kUCKeyActionDisplay = 3
        kUCKeyTranslateNoDeadKeysBit = 0

        Carbon.CFDataGetBytes.argtypes = [CFDataRef] 
        Carbon.CFDataGetBytes.restype = None
        Carbon.CFDataGetLength.argtypes = [CFDataRef]
        Carbon.CFDataGetLength.restype = CFIndex
        Carbon.CFRelease.argtypes = [CFTypeRef]
        Carbon.CFRelease.restype = None
        Carbon.LMGetKbdType.argtypes = []
        Carbon.LMGetKbdType.restype = ctypes.c_uint32
        Carbon.TISCopyCurrentKeyboardInputSource.argtypes = []
        Carbon.TISCopyCurrentKeyboardInputSource.restype = ctypes.c_void_p
        Carbon.TISCopyCurrentASCIICapableKeyboardLayoutInputSource.argtypes = []
        Carbon.TISCopyCurrentASCIICapableKeyboardLayoutInputSource.restype = ctypes.c_void_p
        Carbon.TISGetInputSourceProperty.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        Carbon.TISGetInputSourceProperty.restype = ctypes.c_void_p
        Carbon.UCKeyTranslate.argtypes = [ctypes.c_void_p,
                                          ctypes.c_uint16,
                                          ctypes.c_uint16,
                                          ctypes.c_uint32,
                                          ctypes.c_uint32,
                                          OptionBits,      
                                          ctypes.POINTER(ctypes.c_uint32), 
                                          UniCharCount,    
                                          ctypes.POINTER(UniCharCount), 
                                          UniChar4]
        Carbon.UCKeyTranslate.restype = ctypes.c_uint32

        klis = Carbon.TISCopyCurrentKeyboardInputSource()
        k_layout = Carbon.TISGetInputSourceProperty(klis, kTISPropertyUnicodeKeyLayoutData)
        if k_layout is None:
            klis = Carbon.TISCopyCurrentASCIICapableKeyboardLayoutInputSource()
            k_layout = Carbon.TISGetInputSourceProperty(klis, kTISPropertyUnicodeKeyLayoutData)
        k_layout_size = Carbon.CFDataGetLength(k_layout)
        k_layout_buffer = ctypes.create_string_buffer(k_layout_size) 
        Carbon.CFDataGetBytes(k_layout, CFRange(0, k_layout_size), ctypes.byref(k_layout_buffer))

        for key_code in range(0, 128):
            non_shifted_char = UniChar4()
            shifted_char = UniChar4()
            keys_down = ctypes.c_uint32()
            char_count = UniCharCount()

            retval = Carbon.UCKeyTranslate(k_layout_buffer,
                                           key_code,
                                           kUCKeyActionDisplay,
                                           0, 
                                           Carbon.LMGetKbdType(),
                                           kUCKeyTranslateNoDeadKeysBit,
                                           ctypes.byref(keys_down),
                                           4,
                                           ctypes.byref(char_count),
                                           non_shifted_char)

            non_shifted_key = u''.join(unichr(non_shifted_char[i]) for i in range(char_count.value))

            retval = Carbon.UCKeyTranslate(k_layout_buffer,
                                           key_code,
                                           kUCKeyActionDisplay,
                                           shiftKey >> 8, # Shift
                                           Carbon.LMGetKbdType(),
                                           kUCKeyTranslateNoDeadKeysBit,
                                           ctypes.byref(keys_down),
                                           4,
                                           ctypes.byref(char_count),
                                           shifted_char)

            shifted_key = u''.join(unichr(shifted_char[i]) for i in range(char_count.value))

            self.layout_specific_keys[key_code] = (non_shifted_key, shifted_key)
        Carbon.CFRelease(klis)

    def character_to_vk(self, character):
        for vk in self.non_layout_keys:
            if self.non_layout_keys[vk] == character.lower():
                return (vk, [])
        for vk in self.layout_specific_keys:
            if self.layout_specific_keys[vk][0] == character:
                return (vk, [])
            elif self.layout_specific_keys[vk][1] == character:
                return (vk, ['shift'])
        raise ValueError("Unrecognized character: {}".format(character))

    def vk_to_character(self, vk, modifiers=[]):
        if vk in self.non_layout_keys:
            
            return self.non_layout_keys[vk]
        elif vk in self.layout_specific_keys:
            if 'shift' in modifiers: return self.layout_specific_keys[vk][1]
            return self.layout_specific_keys[vk][0]
        else: raise ValueError("Invalid scan code: {}".format(vk))


class KeyController(object):
    def __init__(self):
        self.key_map = KeyMap()
        self.current_modifiers = {
            "shift": False,
            "caps": False,
            "alt": False,
            "ctrl": False,
            "cmd": False,
        }
        self.media_keys = {
            'KEYTYPE_SOUND_UP': 0,
            'KEYTYPE_SOUND_DOWN': 1,
            'KEYTYPE_BRIGHTNESS_UP': 2,
            'KEYTYPE_BRIGHTNESS_DOWN': 3,
            'KEYTYPE_CAPS_LOCK': 4,
            'KEYTYPE_HELP': 5,
            'POWER_KEY': 6,
            'KEYTYPE_MUTE': 7,
            'UP_ARROW_KEY': 8,
            'DOWN_ARROW_KEY': 9,
            'KEYTYPE_NUM_LOCK': 10,
            'KEYTYPE_CONTRAST_UP': 11,
            'KEYTYPE_CONTRAST_DOWN': 12,
            'KEYTYPE_LAUNCH_PANEL': 13,
            'KEYTYPE_EJECT': 14,
            'KEYTYPE_VIDMIRROR': 15,
            'KEYTYPE_PLAY': 16,
            'KEYTYPE_NEXT': 17,
            'KEYTYPE_PREVIOUS': 18,
            'KEYTYPE_FAST': 19,
            'KEYTYPE_REWIND': 20,
            'KEYTYPE_ILLUMINATION_UP': 21,
            'KEYTYPE_ILLUMINATION_DOWN': 22,
            'KEYTYPE_ILLUMINATION_TOGGLE': 23
        }
    
    def press(self, key_code):
        if key_code >= 128:
            ev = NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
                14, 
                (0, 0), 
                0xa00, 
                0, 
                0, 
                0, 
                8, 
                ((key_code-128) << 16) | (0xa << 8), 
                -1 
            )
            Quartz.CGEventPost(0, ev.CGEvent())
        else:
            event_flags = 0
            if self.current_modifiers["shift"]:
                event_flags += Quartz.kCGEventFlagMaskShift
            if self.current_modifiers["caps"]:
                event_flags += Quartz.kCGEventFlagMaskAlphaShift
            if self.current_modifiers["alt"]:
                event_flags += Quartz.kCGEventFlagMaskAlternate
            if self.current_modifiers["ctrl"]:
                event_flags += Quartz.kCGEventFlagMaskControl
            if self.current_modifiers["cmd"]:
                event_flags += Quartz.kCGEventFlagMaskCommand
            
            if key_code == 0x37: 
                self.current_modifiers["cmd"] = True
            elif key_code == 0x38 or key_code == 0x3C: 
                self.current_modifiers["shift"] = True
            elif key_code == 0x39: 
                self.current_modifiers["caps"] = True
            elif key_code == 0x3A: 
                self.current_modifiers["alt"] = True
            elif key_code == 0x3B: 
                self.current_modifiers["ctrl"] = True
            event = Quartz.CGEventCreateKeyboardEvent(None, key_code, True)
            Quartz.CGEventSetFlags(event, event_flags)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
            time.sleep(0.01)

    def release(self, key_code):
        if key_code >= 128:
            ev = NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
                14, 
                (0, 0), 
                0xb00, 
                0, 
                0, 
                0, 
                8, 
                ((key_code-128) << 16) | (0xb << 8), 
                -1 
            )
            Quartz.CGEventPost(0, ev.CGEvent())
        else:
            if key_code == 0x37: self.current_modifiers["cmd"] = False
            elif key_code == 0x38 or key_code == 0x3C: self.current_modifiers["shift"] = False
            elif key_code == 0x39: self.current_modifiers["caps"] = False
            elif key_code == 0x3A: self.current_modifiers["alt"] = False
            elif key_code == 0x3B: self.current_modifiers["ctrl"] = False

            event_flags = 0
            if self.current_modifiers["shift"]: event_flags += Quartz.kCGEventFlagMaskShift
            if self.current_modifiers["caps"]: event_flags += Quartz.kCGEventFlagMaskAlphaShift
            if self.current_modifiers["alt"]: event_flags += Quartz.kCGEventFlagMaskAlternate
            if self.current_modifiers["ctrl"]: event_flags += Quartz.kCGEventFlagMaskControl
            if self.current_modifiers["cmd"]: event_flags += Quartz.kCGEventFlagMaskCommand
            event = Quartz.CGEventCreateKeyboardEvent(None, key_code, False)
            Quartz.CGEventSetFlags(event, event_flags)
            Quartz.CGEventPost(Quartz.kCGHIDEventTap, event)
            time.sleep(0.01)

    def map_char(self, character):
        if character in self.media_keys: return (128+self.media_keys[character],[])
        else: return self.key_map.character_to_vk(character)
    def map_scan_code(self, scan_code):
        if scan_code >= 128:
            character = [k for k, v in enumerate(self.media_keys) if v == scan_code-128]
            if len(character): return character[0]
            return None
        else: return self.key_map.vk_to_character(scan_code)

class KeyEventListener(object):
    def __init__(self, callback, blocking=False):
        self.blocking = blocking
        self.callback = callback
        self.listening = True
        self.tap = None

    def run(self):
        self.tap = Quartz.CGEventTapCreate(
            Quartz.kCGSessionEventTap,
            Quartz.kCGHeadInsertEventTap,
            Quartz.kCGEventTapOptionDefault,
            Quartz.CGEventMaskBit(Quartz.kCGEventKeyDown) |
            Quartz.CGEventMaskBit(Quartz.kCGEventKeyUp) |
            Quartz.CGEventMaskBit(Quartz.kCGEventFlagsChanged),
            self.handler,
            None)
        loopsource = Quartz.CFMachPortCreateRunLoopSource(None, self.tap, 0)
        loop = Quartz.CFRunLoopGetCurrent()
        Quartz.CFRunLoopAddSource(loop, loopsource, Quartz.kCFRunLoopDefaultMode)
        Quartz.CGEventTapEnable(self.tap, True)

        while self.listening: Quartz.CFRunLoopRunInMode(Quartz.kCFRunLoopDefaultMode, 5, False)

    def handler(self, proxy, e_type, event, refcon):
        scan_code = Quartz.CGEventGetIntegerValueField(event, Quartz.kCGKeyboardEventKeycode)
        key_name = name_from_scancode(scan_code)
        flags = Quartz.CGEventGetFlags(event)
        event_type = ""
        is_keypad = (flags & Quartz.kCGEventFlagMaskNumericPad)
        if e_type == Quartz.kCGEventKeyDown: event_type = "down"
        elif e_type == Quartz.kCGEventKeyUp: event_type = "up"
        elif e_type == Quartz.kCGEventFlagsChanged:
            if key_name.endswith("shift") and (flags & Quartz.kCGEventFlagMaskShift): event_type = "down"
            elif key_name == "caps lock" and (flags & Quartz.kCGEventFlagMaskAlphaShift): event_type = "down"
            elif (key_name.endswith("option") or key_name.endswith("alt")) and (flags & Quartz.kCGEventFlagMaskAlternate): event_type = "down"
            elif key_name == "ctrl" and (flags & Quartz.kCGEventFlagMaskControl): event_type = "down"
            elif key_name == "command" and (flags & Quartz.kCGEventFlagMaskCommand): event_type = "down"
            else: event_type = "up"

        if self.blocking: return None

        self.callback(KeyboardEvent(event_type, scan_code, name=key_name, is_keypad=is_keypad))
        return event

key_controller = KeyController()

def init(): key_controller = KeyController()
def press(scan_code): key_controller.press(scan_code)
def release(scan_code): key_controller.release(scan_code)
def map_name(name): yield key_controller.map_char(name)
def name_from_scancode(scan_code): return key_controller.map_scan_code(scan_code)

def listen(callback):
    if not os.geteuid() == 0: raise OSError("Error 13 - Must be run as administrator")
    KeyEventListener(callback).run()

def type_unicode(character):
    OUTPUT_SOURCE = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)
    event = Quartz.CGEventCreateKeyboardEvent(OUTPUT_SOURCE, 0, True)
    Quartz.CGEventKeyboardSetUnicodeString(event, len(character.encode('utf-16-le')) // 2, character)
    Quartz.CGEventPost(Quartz.kCGSessionEventTap, event)
    event = Quartz.CGEventCreateKeyboardEvent(OUTPUT_SOURCE, 0, False)
    Quartz.CGEventKeyboardSetUnicodeString(event, len(character.encode('utf-16-le')) // 2, character)
    Quartz.CGEventPost(Quartz.kCGSessionEventTap, event)
