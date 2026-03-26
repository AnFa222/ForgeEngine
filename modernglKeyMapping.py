import glfw
from .keys import Key

KEY_MAP = {
    # Letters
    glfw.KEY_A: Key.A, glfw.KEY_B: Key.B, glfw.KEY_C: Key.C, glfw.KEY_D: Key.D,
    glfw.KEY_E: Key.E, glfw.KEY_F: Key.F, glfw.KEY_G: Key.G, glfw.KEY_H: Key.H,
    glfw.KEY_I: Key.I, glfw.KEY_J: Key.J, glfw.KEY_K: Key.K, glfw.KEY_L: Key.L,
    glfw.KEY_M: Key.M, glfw.KEY_N: Key.N, glfw.KEY_O: Key.O, glfw.KEY_P: Key.P,
    glfw.KEY_Q: Key.Q, glfw.KEY_R: Key.R, glfw.KEY_S: Key.S, glfw.KEY_T: Key.T,
    glfw.KEY_U: Key.U, glfw.KEY_V: Key.V, glfw.KEY_W: Key.W, glfw.KEY_X: Key.X,
    glfw.KEY_Y: Key.Y, glfw.KEY_Z: Key.Z,

    # Numbers
    glfw.KEY_0: Key.NUM_0, glfw.KEY_1: Key.NUM_1, glfw.KEY_2: Key.NUM_2,
    glfw.KEY_3: Key.NUM_3, glfw.KEY_4: Key.NUM_4, glfw.KEY_5: Key.NUM_5,
    glfw.KEY_6: Key.NUM_6, glfw.KEY_7: Key.NUM_7, glfw.KEY_8: Key.NUM_8,
    glfw.KEY_9: Key.NUM_9,

    # Numpad
    glfw.KEY_KP_0: Key.KP_0, glfw.KEY_KP_1: Key.KP_1, glfw.KEY_KP_2: Key.KP_2,
    glfw.KEY_KP_3: Key.KP_3, glfw.KEY_KP_4: Key.KP_4, glfw.KEY_KP_5: Key.KP_5,
    glfw.KEY_KP_6: Key.KP_6, glfw.KEY_KP_7: Key.KP_7, glfw.KEY_KP_8: Key.KP_8,
    glfw.KEY_KP_9: Key.KP_9,
    glfw.KEY_KP_ADD: Key.KP_PLUS,
    glfw.KEY_KP_SUBTRACT: Key.KP_MINUS,
    glfw.KEY_KP_MULTIPLY: Key.KP_MULTIPLY,
    glfw.KEY_KP_DIVIDE: Key.KP_DIVIDE,
    glfw.KEY_KP_ENTER: Key.KP_ENTER,
    glfw.KEY_KP_DECIMAL: Key.KP_PERIOD,

    # Function keys
    glfw.KEY_F1: Key.F1, glfw.KEY_F2: Key.F2, glfw.KEY_F3: Key.F3,
    glfw.KEY_F4: Key.F4, glfw.KEY_F5: Key.F5, glfw.KEY_F6: Key.F6,
    glfw.KEY_F7: Key.F7, glfw.KEY_F8: Key.F8, glfw.KEY_F9: Key.F9,
    glfw.KEY_F10: Key.F10, glfw.KEY_F11: Key.F11, glfw.KEY_F12: Key.F12,

    # Arrows
    glfw.KEY_UP: Key.UP, glfw.KEY_DOWN: Key.DOWN,
    glfw.KEY_LEFT: Key.LEFT, glfw.KEY_RIGHT: Key.RIGHT,

    # Modifiers
    glfw.KEY_LEFT_SHIFT: Key.LSHIFT, glfw.KEY_RIGHT_SHIFT: Key.RSHIFT,
    glfw.KEY_LEFT_CONTROL: Key.LCTRL, glfw.KEY_RIGHT_CONTROL: Key.RCTRL,
    glfw.KEY_LEFT_ALT: Key.LALT, glfw.KEY_RIGHT_ALT: Key.RALT,

    # Special
    glfw.KEY_SPACE: Key.SPACE,
    glfw.KEY_ENTER: Key.ENTER,
    glfw.KEY_ESCAPE: Key.ESC,
    glfw.KEY_TAB: Key.TAB,
    glfw.KEY_BACKSPACE: Key.BACKSPACE,
    glfw.KEY_CAPS_LOCK: Key.CAPSLOCK,

    # Navigation
    glfw.KEY_INSERT: Key.INSERT,
    glfw.KEY_DELETE: Key.DELETE,
    glfw.KEY_HOME: Key.HOME,
    glfw.KEY_END: Key.END,
    glfw.KEY_PAGE_UP: Key.PAGEUP,
    glfw.KEY_PAGE_DOWN: Key.PAGEDOWN,

    # Symbols
    glfw.KEY_MINUS: Key.MINUS,
    glfw.KEY_EQUAL: Key.EQUALS,
    glfw.KEY_LEFT_BRACKET: Key.LEFTBRACKET,
    glfw.KEY_RIGHT_BRACKET: Key.RIGHTBRACKET,
    glfw.KEY_BACKSLASH: Key.BACKSLASH,
    glfw.KEY_SEMICOLON: Key.SEMICOLON,
    glfw.KEY_APOSTROPHE: Key.APOSTROPHE,
    glfw.KEY_COMMA: Key.COMMA,
    glfw.KEY_PERIOD: Key.PERIOD,
    glfw.KEY_SLASH: Key.SLASH,
    glfw.KEY_GRAVE_ACCENT: Key.GRAVE,
}