from enum import IntEnum, auto

class Key(IntEnum):
    # Letters
    A=auto(); B=auto(); C=auto(); D=auto(); E=auto(); F=auto(); G=auto()
    H=auto(); I=auto(); J=auto(); K=auto(); L=auto(); M=auto(); N=auto()
    O=auto(); P=auto(); Q=auto(); R=auto(); S=auto(); T=auto(); U=auto()
    V=auto(); W=auto(); X=auto(); Y=auto(); Z=auto()

    # Numbers
    NUM_0=auto(); NUM_1=auto(); NUM_2=auto(); NUM_3=auto(); NUM_4=auto()
    NUM_5=auto(); NUM_6=auto(); NUM_7=auto(); NUM_8=auto(); NUM_9=auto()

    # Numpad
    KP_0=auto(); KP_1=auto(); KP_2=auto(); KP_3=auto(); KP_4=auto()
    KP_5=auto(); KP_6=auto(); KP_7=auto(); KP_8=auto(); KP_9=auto()
    KP_PLUS=auto(); KP_MINUS=auto(); KP_MULTIPLY=auto(); KP_DIVIDE=auto()
    KP_ENTER=auto(); KP_PERIOD=auto()

    # Function keys
    F1=auto(); F2=auto(); F3=auto(); F4=auto(); F5=auto(); F6=auto()
    F7=auto(); F8=auto(); F9=auto(); F10=auto(); F11=auto(); F12=auto()

    # Arrows
    UP=auto(); DOWN=auto(); LEFT=auto(); RIGHT=auto()

    # Modifiers
    LSHIFT=auto(); RSHIFT=auto()
    LCTRL=auto(); RCTRL=auto()
    LALT=auto(); RALT=auto()

    # Special
    SPACE=auto()
    ENTER=auto()
    ESC=auto()
    TAB=auto()
    BACKSPACE=auto()
    CAPSLOCK=auto()

    # Navigation
    INSERT=auto()
    DELETE=auto()
    HOME=auto()
    END=auto()
    PAGEUP=auto()
    PAGEDOWN=auto()

    # Symbols
    MINUS=auto()
    EQUALS=auto()
    LEFTBRACKET=auto()
    RIGHTBRACKET=auto()
    BACKSLASH=auto()
    SEMICOLON=auto()
    APOSTROPHE=auto()
    COMMA=auto()
    PERIOD=auto()
    SLASH=auto()
    GRAVE=auto()

    # Mouse buttons
    MOUSE_LEFT=auto()
    MOUSE_MIDDLE=auto()
    MOUSE_RIGHT=auto()