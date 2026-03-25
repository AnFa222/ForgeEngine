from enum import auto
class TextRenderer:
    def __init__(self, text, font_path, font_size, color, layer, alpha=255):
        self.text = text
        self.font_path = font_path
        self.font_size = font_size
        self.color = color
        self.layer = layer
        self.alpha = alpha
        self.always_render = False
        self.visible = True
        self.dirty = True
        self.is_overlay = False
        self.cache_id = auto()

    def update_properties(self):
        self.dirty = True