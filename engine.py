from .window import Window
from .keys import Key
from .events import Event
from .time import Time
import time
from .checkCollision import check_collision_all
from .log import error
from .utils import check_on_screen
import sys
import os

IS_BUILD = hasattr(sys, "_MEIPASS")

class Engine:
    def __init__(self):
        self.window = Window(None, None, None)
        self.time = Time()
        self.running = False
        self.objects = []
        self.deltaTime = 0.0
        self.pressed_keys = set()
        self.frame_pressed_keys = set()
        self.frame_released_keys = set()
        self.camera = None
        self.cameras = {}
        self.debug = False

        if IS_BUILD:
            print("Running in build mode.")

    def add_object(self, obj):
        self.objects.append(obj)

    def get_path(self, relative_path):
        if IS_BUILD:
            return os.path.join(sys._MEIPASS, relative_path)
        else:
            return relative_path

    def send_object_updates(self):
        for obj in self.objects:
            obj.update()

    def send_object_start(self):
        for obj in self.objects:
            obj.start()

    def send_object_early_updates(self):
        for obj in self.objects:
            obj.early_update()

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
        for obj in self.objects:
            if obj.renderer and obj.renderer.visible:
                self.window.schedule_blit(obj.renderer.image_id, (obj.transform.x, obj.transform.y), obj.transform.rotation, obj.transform.scale_x, obj.transform.scale_y, obj.renderer.alpha, obj.renderer.layer, self.camera, obj.renderer.always_render, obj.renderer.cache_id, obj.renderer.dirty, obj.renderer.is_overlay)
            
            if obj.textRenderer and obj.textRenderer.visible:
                self.window.schedule_draw_text(obj.textRenderer.text, self.get_path(obj.textRenderer.font_path), obj.textRenderer.font_size, obj.textRenderer.color, (obj.transform.x, obj.transform.y), obj.transform.rotation, obj.transform.scale_x, obj.transform.scale_y, obj.textRenderer.alpha, obj.textRenderer.layer, self.camera, obj.textRenderer.cache_id, obj.textRenderer.always_render, obj.textRenderer.is_overlay, obj.textRenderer.dirty)


            if self.debug and obj.collider:
                if hasattr(obj.collider.shape, 'width') and hasattr(obj.collider.shape, 'height'):
                    from .checkCollision import get_rect_corners
                    corners = get_rect_corners(obj, obj.collider)
                    self.window.schedule_draw_polygon(corners, (255, 0, 0), 2, 999, self.camera)
                elif hasattr(obj.collider.shape, 'points'):
                    from .checkCollision import get_polygon_world_points
                    points = get_polygon_world_points(obj, obj.collider)
                    self.window.schedule_draw_polygon(points, (0, 255, 255), 2, 999, self.camera)

        self.window.blit()
        self.window.draw_debug_shapes()

    def get_cameras(self):
        for obj in self.objects:
            if obj.camera:
                if obj.camera.camera_id in self.cameras:
                    error(f"Multiple cameras with ID {obj.camera.camera_id}. Only the first will be used.")
                self.cameras[obj.camera.camera_id] = obj


        if len(self.cameras) == 0:
            error("No cameras found in the scene. Rendering may not work correctly.")
        self.use_camera(next(iter(self.cameras.keys())))

    def use_camera(self, camera_id):
        if camera_id in self.cameras:
            self.camera = self.cameras[camera_id]

    def main_loop(self):
        self.check_incompatible_components()

        self.get_cameras()
        self.send_object_start()
        self.last_time = time.time()
        self.running = True

        while self.running:
            if Event.QUIT in self.window.get_events():
                self.running = False

            self.deltaTime = time.time() - self.last_time
            self.last_time = time.time()

            self.handle_input()
            self.time.update(self.deltaTime)
            self.send_object_early_updates()
            self.send_object_updates()
            self.window.clear_screen()
            self.render_objects()
            self.window.update_screen()

        print("----------------------------------")

    def import_image(self, path, image_id):
        actual_path = self.get_path(path)
        return self.window.load_image(actual_path, image_id)
    
    def handle_input(self):
        self.frame_pressed_keys.clear()
        self.frame_released_keys.clear()

        current_pressed = self.window.get_keyboard_input()

        for key in current_pressed:
            if key not in self.pressed_keys:
                self.frame_pressed_keys.add(key)

        for key in self.pressed_keys:
            if key not in current_pressed:
                self.frame_released_keys.add(key)

        self.pressed_keys = current_pressed

    def check_collision(self, obj, objs):
        visible_objs = [
            o for o in objs
            if check_on_screen((o.transform.x, o.transform.y), 
                            o.collider.shape.width if o.collider and hasattr(o.collider.shape, 'width') else 0,
                            o.collider.shape.height if o.collider and hasattr(o.collider.shape, 'height') else 0,
                            self.camera)
        ]

        if obj.collider:
            return check_collision_all(obj, visible_objs)
        return False
    
    def destroy(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)
        else:
            error(f"Attempted to destroy and invalid object {obj}.")