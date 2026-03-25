import pyglet
from pyglet import shapes
from .keyMapping import KEY_MAP
from .events import Event
from .log import error
from .transformations import rotate
from .utils import check_on_screen

class Window:
    def __init__(self, width, height, title):
        self.width = width
        self.height = height
        self.title = title
        self.preprocessed_images = {}
        self.images = {}
        self.blit_schedule = []
        self.draw_schedule = []

        self.window = None
        self.batch = pyglet.graphics.Batch()
        self.keys = None
        self.key_map_rev = {v: k for k, v in KEY_MAP.items()}

    def initialize(self):
        self.window = pyglet.window.Window(self.width, self.height, self.title)
        self.keys = pyglet.window.key.KeyStateHandler()
        self.window.push_handlers(self.keys)

    def get_keyboard_input(self):
        pressed_keys = set()
        for eng_key, pg_key in self.key_map_rev.items():
            if self.keys[pg_key]:
                pressed_keys.add(eng_key)
        return pressed_keys

    def get_events(self):
        events = set()

        def on_close():
            events.add(Event.QUIT)
        self.window.push_handlers(on_close=on_close)

        return events

    def process_image(self, image_id, scalex, scaley, rotation, alpha, cache_id):
        image = self.preprocessed_images[image_id]
        img = image.get_texture()
        img.width = int(img.width * scalex)
        img.height = int(img.height * scaley)
        sprite = pyglet.sprite.Sprite(img, batch=self.batch)
        sprite.rotation = rotation
        sprite.opacity = alpha
        self.images[cache_id] = sprite

    def schedule_draw_text(self, text, font_path, font_size, color, position, rotation, scalex, scaley, alpha, layer, camera, cache_id, always_render, is_overlay, is_dirty):
        if cache_id in self.images and not is_dirty:
            sprite = self.images[cache_id]
        else:
            try:
                font = pyglet.font.load('', size=font_size)
                label = pyglet.text.Label(
                    text,
                    font_name=font.name,
                    font_size=font_size,
                    color=color + (alpha,),
                    x=position[0],
                    y=position[1],
                    anchor_x='center',
                    anchor_y='center'
                )
                self.images[cache_id] = label
            except Exception as e:
                error(f"Error rendering text '{text}': {e}. Text will not be rendered.")
                return
            sprite = self.images[cache_id]

        if not is_overlay:
            pos = (position[0] - camera.transform.x, position[1] - camera.transform.y)
        else:
            pos = position

        self.blit_schedule.append((sprite, pos, layer))

    def schedule_blit(self, image_id, position, rotation, scalex, scaley, alpha, layer, camera, always_render, cache_id, is_dirty, is_overlay):
        image = self.preprocessed_images.get(image_id)
        image_width = image.width * scalex
        image_height = image.height * scaley

        if not check_on_screen(position, image_width, image_height, camera) and not always_render and not is_overlay:
            return
        
        if cache_id not in self.images or is_dirty:
            self.process_image(image_id, scalex, scaley, rotation, alpha, cache_id)

        sprite = self.images[cache_id]

        if not is_overlay:
            screen_x = position[0] - camera.transform.x
            screen_y = position[1] - camera.transform.y
        else:
            screen_x = position[0]
            screen_y = position[1]

        sprite.x = screen_x
        sprite.y = screen_y
        sprite.rotation = rotation
        sprite.opacity = alpha

        self.blit_schedule.append((sprite, (screen_x, screen_y), layer))

    def blit(self):
        self.blit_schedule.sort(key=lambda x: x[2])
        for sprite, _, _ in self.blit_schedule:
            if isinstance(sprite, pyglet.text.Label):
                sprite.draw()
            else:
                sprite.draw()
        self.blit_schedule.clear()

    def schedule_draw_polygon(self, points, color, width, layer, camera):
        screen_points = [(x - camera.transform.x, y - camera.transform.y) for x, y in points]
        self.draw_schedule.append(("polygon", screen_points, color, width, layer))

    def schedule_draw_circle(self, center, radius, color, width, layer, camera):
        screen_x = center[0] - camera.transform.x
        screen_y = center[1] - camera.transform.y
        self.draw_schedule.append(("circle", (screen_x, screen_y), radius, color, width, layer))

    def draw_debug_shapes(self):
        self.draw_schedule.sort(key=lambda x: x[4])
        for item in self.draw_schedule:
            shape_type = item[0]
            if shape_type == "polygon":
                _, points, color, width, _ = item
                if len(points) >= 2:
                    pyglet.graphics.draw(
                        len(points), pyglet.gl.GL_LINE_LOOP if width else pyglet.gl.GL_POLYGON,
                        ('v2f', sum(points, ())),
                        ('c3B', color * len(points))
                    )
            elif shape_type == "circle":
                _, center, radius, color, width, _ = item
                segments = 32
                verts = []
                for i in range(segments):
                    angle = 2 * 3.14159 * i / segments
                    x = center[0] + radius * pyglet.math.cos(angle)
                    y = center[1] + radius * pyglet.math.sin(angle)
                    verts.extend([x, y])
                pyglet.graphics.draw(
                    segments, pyglet.gl.GL_LINE_LOOP if width else pyglet.gl.GL_POLYGON,
                    ('v2f', verts),
                    ('c3B', color * segments)
                )
        self.draw_schedule.clear()

    def clear_screen(self):
        self.window.clear()

    def update_screen(self):
        pass

    def load_image(self, path, image_id):
        try:
            image = pyglet.image.load(path)
            self.preprocessed_images[image_id] = image
        except Exception as e:
            error(f"Error loading image '{path}': {e}. Rendering may not work correctly.")
