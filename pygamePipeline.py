import pygame
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
        self.audio = {}

    def load_audio(self, path, audio_id):
        try:
            sound = pygame.mixer.Sound(path)
            self.audio[audio_id] = sound
        except Exception as e:
            error(f"Error loading audio '{path}': {e}. Audio may not work correctly.")

    def play_audio(self, audio_id):
        if audio_id in self.audio:
            self.audio[audio_id].play()
        else:
            error(f"Audio ID {audio_id} not found in audio library. Cannot play audio.")

    def stop_audio(self, audio_id):
        if audio_id in self.audio:
            self.audio[audio_id].stop()
        else:
            error(f"Audio ID {audio_id} not found in audio library. Cannot stop audio.")
        

    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def get_keyboard_input(self):
        pygame_keys = pygame.key.get_pressed()

        return pygame_keys
    
    def get_mouse_input(self):
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_position = pygame.mouse.get_pos()

        return mouse_buttons, mouse_position
    
    def get_events(self):
        events = set()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.add(Event.QUIT)

        return events

    
    def process_image(self, image_id, scalex, scaley, rotation, alpha, cache_id):
        image = self.preprocessed_images[image_id].copy()

        if scalex != 1.0 or scaley != 1.0:
            width = int(image.get_width() * scalex)
            height = int(image.get_height() * scaley)
            image = pygame.transform.scale(image, (width, height))

        if rotation != 0:
            image = pygame.transform.rotate(image, rotation)

        if alpha != 255:
            image.set_alpha(alpha)

        self.images[cache_id] = image

    def schedule_draw_text(self, text, font_path, font_size, color, position, rotation, scalex, scaley, alpha, layer, camera, cache_id, always_render, is_overlay, is_dirty):
        if cache_id in self.images and not is_dirty:
            image = self.images[cache_id]
        else:
            try:
                font = pygame.font.Font(font_path, font_size)
                image = font.render(text, True, color)
                self.images[cache_id] = image
            except Exception as e:
                error(f"Error rendering text '{text}': {e}. Text will not be rendered.")
                return
            
        if is_overlay:
            position = position
        else:
            position = (position[0] - camera.transform.x, position[1] - camera.transform.y)

        self.blit_schedule.append((image, position, layer))
        


    def schedule_blit(self, obj, position, rotation=0, scalex=1, scaley=1, alpha=255,
                    layer=0, camera=None, always_render=False, cache_id=None, is_dirty=False, is_overlay=False):
        #obj: either an int (image_id) or a mesh [[image_id, offset_x, offset_y], ...]
        if isinstance(obj, int):
            mesh = [[obj, 0, 0]]
        else:
            mesh = obj

        for image_id, offset_x, offset_y in mesh:
            quad_pos = (position[0] + offset_x, position[1] + offset_y)

            image = self.preprocessed_images.get(image_id)
            image_width = image.get_width() * scalex
            image_height = image.get_height() * scaley

            if not check_on_screen(quad_pos, image_width, image_height, camera) and not always_render and not is_overlay:
                continue

            if cache_id not in self.images or is_dirty:
                self.process_image(image_id, scalex, scaley, rotation, alpha, cache_id)
            image = self.images[cache_id]

            if not is_overlay:
                screen_x = quad_pos[0] - camera.transform.x
                screen_y = quad_pos[1] - camera.transform.y
            else:
                screen_x = quad_pos[0]
                screen_y = quad_pos[1]

            rect = image.get_rect(center=(screen_x, screen_y))
            self.blit_schedule.append((image, rect.topleft, layer))
    
    def set_mouse_pos(self, position):
        pygame.mouse.set_pos(position)

    def show_mouse(self):
        pygame.mouse.set_visible(True)

    def hide_mouse(self):
        pygame.mouse.set_visible(False)

    def blit(self):
        self.blit_schedule.sort(key=lambda x: x[2])
        for image, position, _ in self.blit_schedule:
            self.screen.blit(image, position)
        self.blit_schedule.clear()

    def schedule_draw_polygon(self, points, color, width, layer, camera):
        screen_points = []
        for x, y in points:
            screen_x = x - camera.transform.x
            screen_y = y - camera.transform.y
            screen_points.append((screen_x, screen_y))

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
                    pygame.draw.polygon(self.screen, color, points, width)
            elif shape_type == "circle":
                _, center, radius, color, width, _ = item
                pygame.draw.circle(self.screen, color, (int(center[0]), int(center[1])), int(radius), width)
        self.draw_schedule.clear()

    def clear_screen(self, background_color):
        self.screen.fill(background_color)

    def update_screen(self):
        pygame.display.flip()

    def load_image(self, path, image_id):
        try:
            image = pygame.image.load(path).convert_alpha()
            self.preprocessed_images[image_id] = image
        except Exception as e:
            error(f"Error loading image '{path}': {e}. Rendering may not work correctly.")

            
    def poll_events(self):
        pygame.event.pump()