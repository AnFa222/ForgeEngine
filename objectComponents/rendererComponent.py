from enum import auto
class Renderer:
    def __init__(self, image_id, layer, alpha=255):
        self.image_id = image_id
        self.layer = layer
        self.alpha = alpha
        self.always_render = False
        self.visible = True
        self.dirty = True
        self.is_overlay = False
        self.cache_id = auto()

    def update_properties(self):
        self.dirty = True