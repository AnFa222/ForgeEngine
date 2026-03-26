import pygame
from .keys import Key

KEY_MAP = {
    # Letters
    pygame.K_a: Key.A, pygame.K_b: Key.B, pygame.K_c: Key.C, pygame.K_d: Key.D,
    pygame.K_e: Key.E, pygame.K_f: Key.F, pygame.K_g: Key.G, pygame.K_h: Key.H,
    pygame.K_i: Key.I, pygame.K_j: Key.J, pygame.K_k: Key.K, pygame.K_l: Key.L,
    pygame.K_m: Key.M, pygame.K_n: Key.N, pygame.K_o: Key.O, pygame.K_p: Key.P,
    pygame.K_q: Key.Q, pygame.K_r: Key.R, pygame.K_s: Key.S, pygame.K_t: Key.T,
    pygame.K_u: Key.U, pygame.K_v: Key.V, pygame.K_w: Key.W, pygame.K_x: Key.X,
    pygame.K_y: Key.Y, pygame.K_z: Key.Z,

    # Numbers
    pygame.K_0: Key.NUM_0, pygame.K_1: Key.NUM_1, pygame.K_2: Key.NUM_2,
    pygame.K_3: Key.NUM_3, pygame.K_4: Key.NUM_4, pygame.K_5: Key.NUM_5,
    pygame.K_6: Key.NUM_6, pygame.K_7: Key.NUM_7, pygame.K_8: Key.NUM_8,
    pygame.K_9: Key.NUM_9,

    # Numpad
    pygame.K_KP0: Key.KP_0, pygame.K_KP1: Key.KP_1, pygame.K_KP2: Key.KP_2,
    pygame.K_KP3: Key.KP_3, pygame.K_KP4: Key.KP_4, pygame.K_KP5: Key.KP_5,
    pygame.K_KP6: Key.KP_6, pygame.K_KP7: Key.KP_7, pygame.K_KP8: Key.KP_8,
    pygame.K_KP9: Key.KP_9,
    pygame.K_KP_PLUS: Key.KP_PLUS,
    pygame.K_KP_MINUS: Key.KP_MINUS,
    pygame.K_KP_MULTIPLY: Key.KP_MULTIPLY,
    pygame.K_KP_DIVIDE: Key.KP_DIVIDE,
    pygame.K_KP_ENTER: Key.KP_ENTER,
    pygame.K_KP_PERIOD: Key.KP_PERIOD,

    # Function keys
    pygame.K_F1: Key.F1, pygame.K_F2: Key.F2, pygame.K_F3: Key.F3,
    pygame.K_F4: Key.F4, pygame.K_F5: Key.F5, pygame.K_F6: Key.F6,
    pygame.K_F7: Key.F7, pygame.K_F8: Key.F8, pygame.K_F9: Key.F9,
    pygame.K_F10: Key.F10, pygame.K_F11: Key.F11, pygame.K_F12: Key.F12,

    # Arrows
    pygame.K_UP: Key.UP, pygame.K_DOWN: Key.DOWN,
    pygame.K_LEFT: Key.LEFT, pygame.K_RIGHT: Key.RIGHT,

    # Modifiers
    pygame.K_LSHIFT: Key.LSHIFT, pygame.K_RSHIFT: Key.RSHIFT,
    pygame.K_LCTRL: Key.LCTRL, pygame.K_RCTRL: Key.RCTRL,
    pygame.K_LALT: Key.LALT, pygame.K_RALT: Key.RALT,

    # Special
    pygame.K_SPACE: Key.SPACE,
    pygame.K_RETURN: Key.ENTER,
    pygame.K_ESCAPE: Key.ESC,
    pygame.K_TAB: Key.TAB,
    pygame.K_BACKSPACE: Key.BACKSPACE,
    pygame.K_CAPSLOCK: Key.CAPSLOCK,

    # Navigation
    pygame.K_INSERT: Key.INSERT,
    pygame.K_DELETE: Key.DELETE,
    pygame.K_HOME: Key.HOME,
    pygame.K_END: Key.END,
    pygame.K_PAGEUP: Key.PAGEUP,
    pygame.K_PAGEDOWN: Key.PAGEDOWN,

    # Symbols
    pygame.K_MINUS: Key.MINUS,
    pygame.K_EQUALS: Key.EQUALS,
    pygame.K_LEFTBRACKET: Key.LEFTBRACKET,
    pygame.K_RIGHTBRACKET: Key.RIGHTBRACKET,
    pygame.K_BACKSLASH: Key.BACKSLASH,
    pygame.K_SEMICOLON: Key.SEMICOLON,
    pygame.K_QUOTE: Key.APOSTROPHE,
    pygame.K_COMMA: Key.COMMA,
    pygame.K_PERIOD: Key.PERIOD,
    pygame.K_SLASH: Key.SLASH,
    pygame.K_BACKQUOTE: Key.GRAVE,
}