from .keys import Key
from .events import Event
from .time import Time
import time
from .checkCollision import check_collision_all
from .log import error
from .utils import check_on_screen
import sys
import os
from .pipelines import pygamePipeline, modernGlPipeline

IS_BUILD = hasattr(sys, "_MEIPASS")

class Engine:
    def __init__(self, render_pipeline):
        self.render_pipeline = render_pipeline
        if self.render_pipeline == pygamePipeline:
            from .pygamePipeline import Window as PygameRenderer
            from .pygameKeyMapping import KEY_MAP as PYGAME_KEY_MAP
            from .pygameKeyMapping import MOUSE_BUTTON_MAP as PYGAME_MOUSE_BUTTON_MAP
            self.window = PygameRenderer(None, None, None)
            self.key_map = PYGAME_KEY_MAP
            self.mouse_map = PYGAME_MOUSE_BUTTON_MAP
        elif self.render_pipeline == modernGlPipeline:
            from .modernglPipeline import Window as ModernglRenderer
            from .modernglKeyMapping import KEY_MAP as MODERNGL_KEY_MAP
            from .modernglKeyMapping import MOUSE_BUTTON_MAP as MODERNGL_MOUSE_BUTTON_MAP
            self.window = ModernglRenderer(None, None, None)
            self.key_map = MODERNGL_KEY_MAP
            self.mouse_map = MODERNGL_MOUSE_BUTTON_MAP
        else:
            error("No valid render pipeline chosen.")
            sys.exit(1)
        
        self.time = Time()
        self.running = False
        self.scenes = {}
        self.current_scene = None
        self.objects = []
        self.background_color = (0, 0, 0)
        self.deltaTime = 0.0
        self.pressed_keys = set()
        self.frame_pressed_keys = set()
        self.frame_released_keys = set()
        self.screen_mouse_position = (0, 0)
        self.world_mouse_position = (0, 0)
        self.pressed_mouse_buttons = set()
        self.frame_pressed_mouse_buttons = set()
        self.frame_released_mouse_buttons = set()
        self.camera = None
        self.objects_to_destroy = []
        self.cameras = {}
        self.debug = False

        self.has_audio_components = []
        self.has_camera_components = []
        self.has_collider_components = []
        self.has_renderer_components = []
        self.has_text_renderer_components = []
        self.has_kinematic_components = []
        self.has_transform_components = []

        if IS_BUILD:
            print("Running in build mode.")

    def get_components(self):
        self.has_audio_components = []
        self.has_camera_components = []
        self.has_collider_components = []
        self.has_renderer_components = []
        self.has_text_renderer_components = []
        self.has_kinematic_components = []
        self.has_transform_components = []

        for obj in self.objects:
            if obj.active:
                if obj.audio:
                    self.has_audio_components.append(obj)
                if obj.camera:
                    self.has_camera_components.append(obj)
                if obj.collider:
                    self.has_collider_components.append(obj)
                if obj.renderer:
                    self.has_renderer_components.append(obj)
                if obj.textRenderer:
                    self.has_text_renderer_components.append(obj)
                if obj.kinematic:
                    self.has_kinematic_components.append(obj)
                if obj.transform:
                    self.has_transform_components.append(obj)

    def add_scene(self, scene):
        self.scenes[scene.scene_id] = scene

    def load_scene(self, scene_id):
        if scene_id in self.scenes:
            self.current_scene = self.scenes[scene_id]
            self.objects = self.current_scene.objects
            self.background_color = self.current_scene.background_color
        else:
            error(f"Scene with ID {scene_id} not found. Cannot load scene.")

    def set_mouse_position(self, position):
        self.window.set_mouse_pos(position)

    def show_mouse(self):
        self.window.show_mouse()

    def hide_mouse(self):
        self.window.hide_mouse()

    def get_path(self, relative_path):
        if IS_BUILD:
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            return relative_path

    def send_object_updates(self):
        for obj in self.objects:
            if obj.active:
                obj.update()

    def send_object_start(self):
        for obj in self.objects:
            if obj.active:
                obj.start()

    def send_object_early_updates(self):
        for obj in self.objects:
            if obj.active:
                obj.early_update()

    def update_physics(self):
        for obj in self.has_kinematic_components:
            obj.kinematic.update(obj, self)

    def check_incompatible_components(self):
        for obj in self.objects:
            if obj.renderer and not obj.transform:
                error(f"Object {obj} has a renderer but no transform. Object renderer will be ignored.")
                obj.renderer = None

            if obj.collider and not obj.transform:
                error(f"Object {obj} has a collider but no transform. Object collider will be ignored.")
                obj.collider = None

            if obj.camera and not obj.transform:
                error(f"Object {obj} has a camera but no transform. Object camera will be ignored.")
                obj.camera = None

            if obj.camera and (obj.collider or obj.renderer):
                error(f"Object {obj} has a camera but also has a collider or renderer. Extra components will be ignored.")
                obj.collider = None
                obj.renderer = None


    def render_objects(self):
        for obj in self.has_renderer_components:
            self.window.schedule_blit(obj.renderer.image_id, (obj.transform.x, obj.transform.y), obj.transform.rotation, obj.transform.scale_x, obj.transform.scale_y, obj.renderer.alpha, obj.renderer.layer, self.camera, obj.renderer.always_render, obj.renderer.cache_id, obj.renderer.dirty, obj.renderer.is_overlay)

            if self.debug and obj.collider:
                if hasattr(obj.collider.shape, 'width') and hasattr(obj.collider.shape, 'height'):
                    from .checkCollision import get_rect_corners
                    corners = get_rect_corners(obj, obj.collider)
                    self.window.schedule_draw_polygon(corners, (255, 0, 0), 2, 999, self.camera)
                elif hasattr(obj.collider.shape, 'points'):
                    from .checkCollision import get_polygon_world_points
                    points = get_polygon_world_points(obj, obj.collider)
                    self.window.schedule_draw_polygon(points, (0, 255, 255), 2, 999, self.camera)

        for obj in self.has_text_renderer_components:
            self.window.schedule_draw_text(obj.textRenderer.text, self.get_path(obj.textRenderer.font_path), obj.textRenderer.font_size, obj.textRenderer.color, (obj.transform.x, obj.transform.y), obj.transform.rotation, obj.transform.scale_x, obj.transform.scale_y, obj.textRenderer.alpha, obj.textRenderer.layer, self.camera, obj.textRenderer.cache_id, obj.textRenderer.always_render, obj.textRenderer.is_overlay, obj.textRenderer.dirty)


        self.window.blit()
        self.window.draw_debug_shapes()

    def get_cameras(self):
        for obj in self.has_camera_components:
            if obj.camera.camera_id in self.cameras:
                error(f"Multiple cameras with ID {obj.camera.camera_id}. Only the first will be used.")
            self.cameras[obj.camera.camera_id] = obj


        if len(self.cameras) == 0:
            error("No cameras found in the scene. Rendering may not work correctly.")
        self.use_camera(next(iter(self.cameras.keys())))

    def use_camera(self, camera_id):
        if camera_id in self.cameras:
            self.camera = self.cameras[camera_id]

    def handle_object_audio(self):
        for obj in self.has_audio_components:
            if obj.audio.play:
                if obj.audio.audio_id in self.window.audio:
                    self.window.play_audio(obj.audio.audio_id)
                else:
                    error(f"Audio ID {obj.audio.audio_id} not found in audio library. Cannot play audio.")
            if obj.audio.stop:
                if obj.audio.audio_id in self.window.audio:
                    self.window.stop_audio(obj.audio.audio_id)
                else:
                    error(f"Audio ID {obj.audio.audio_id} not found in audio library. Cannot stop audio.")
            
            obj.audio.play = False
            obj.audio.stop = False


    def main_loop(self):
        if self.current_scene is None:
             error("No scene loaded. Please load a scene before starting the main loop.")
             return
        
        if self.debug:
            self.check_incompatible_components()

        self.get_components()

        self.get_cameras()
        self.send_object_start()
        self.last_time = time.time()
        self.running = True

        while self.running:
            self.window.poll_events()
            if Event.QUIT in self.window.get_events():
                self.running = False

            self.get_components()

            self.deltaTime = time.time() - self.last_time
            self.last_time = time.time()

            self.destroy_objects()
            self.handle_input()
            self.time.update(self.deltaTime)
            self.send_object_early_updates()
            self.update_physics()
            self.send_object_updates()
            self.window.clear_screen(self.background_color)
            self.render_objects()
            self.window.update_screen()
            self.handle_object_audio()

        print("----------------------------------")

    def import_image(self, path, image_id):
        actual_path = self.get_path(path)
        return self.window.load_image(actual_path, image_id)
    
    def import_audio(self, path, audio_id):
        actual_path = self.get_path(path)
        self.window.load_audio(actual_path, audio_id)

    def get_key(self, key):
        return key in self.pressed_keys
    def get_key_down(self, key):
        return key in self.frame_pressed_keys
    def get_key_up(self, key):
        return key in self.frame_released_keys
    def get_mouse_button(self, button):
        return button in self.pressed_mouse_buttons
    def get_mouse_button_down(self, button):
        return button in self.frame_pressed_mouse_buttons
    def get_mouse_button_up(self, button):
        return button in self.frame_released_mouse_buttons
    
    def handle_input(self):
        self.frame_pressed_keys.clear()
        self.frame_released_keys.clear()
        self.frame_pressed_mouse_buttons.clear()
        self.frame_released_mouse_buttons.clear()

        current_pressed_unmapped = self.window.get_keyboard_input()
        current_pressed = set()

        current_mouse_pressed_unmapped, current_mouse_position = self.window.get_mouse_input()
        self.screen_mouse_position = current_mouse_position
        self.world_mouse_position = (current_mouse_position[0] + self.camera.transform.x, current_mouse_position[1] + self.camera.transform.y)
        current_mouse_pressed = set()

        #Handle Keyboard
        for unmapped_key, mapped_key in self.key_map.items():
            if current_pressed_unmapped[unmapped_key]:
                current_pressed.add(mapped_key)

        for key in current_pressed:
            if key not in self.pressed_keys:
                self.frame_pressed_keys.add(key)

        for key in self.pressed_keys:
            if key not in current_pressed:
                self.frame_released_keys.add(key)

        self.pressed_keys = current_pressed

        #Handle Mouse
        for unmapped_button, mapped_button in self.mouse_map.items():
            if current_mouse_pressed_unmapped[unmapped_button - 1]:
                current_mouse_pressed.add(mapped_button)

        for button in current_mouse_pressed:
            if button not in self.pressed_mouse_buttons:
                self.frame_pressed_mouse_buttons.add(button)

        for button in self.pressed_mouse_buttons:
            if button not in current_mouse_pressed:
                self.frame_released_mouse_buttons.add(button)

        self.pressed_mouse_buttons = current_mouse_pressed

    def check_collision(self, obj, objs):
        visible_objs = [
            o for o in objs
            if o.active and check_on_screen((o.transform.x, o.transform.y), 
                            o.collider.shape.width if o.collider and hasattr(o.collider.shape, 'width') else 0,
                            o.collider.shape.height if o.collider and hasattr(o.collider.shape, 'height') else 0,
                            self.camera)
        ]

        if obj.collider and obj.active:
            return check_collision_all(obj, visible_objs)
        return False
    
    def destroy_objects(self):
        for obj in self.current_scene.objects_to_destroy:
            if obj in self.current_scene.objects:
                self.current_scene.objects.remove(obj)
        self.current_scene.objects_to_destroy.clear()

    