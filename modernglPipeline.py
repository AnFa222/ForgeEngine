import glfw
import moderngl
import numpy as np
from PIL import Image
from .events import Event
from .log import error
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
        self.ctx = None
        self.textures = {}
        self.audio = {}

    def poll_events(self):
        glfw.poll_events()

    def load_audio(self, path, audio_id):
        pass

    def play_audio(self, audio_id):
        pass

    def stop_audio(self, audio_id):
        pass

    def set_finished_audio(self):
        pass

    def initialize(self):
        if not glfw.init():
            raise Exception("GLFW init failed")

        self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        glfw.make_context_current(self.window)

        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.BLEND)

        self.prog = self.ctx.program(
            vertex_shader='''
                #version 330
                in vec2 in_pos;
                in vec2 in_uv;

                uniform vec2 offset;
                uniform vec2 scale;

                out vec2 uv;

                void main() {
                    vec2 pos = in_pos * scale + offset;
                    gl_Position = vec4(pos, 0.0, 1.0);
                    uv = in_uv;
                }
            ''',
            fragment_shader='''
                #version 330
                uniform sampler2D tex;
                in vec2 uv;
                out vec4 fragColor;

                void main() {
                    fragColor = texture(tex, uv);
                }
            '''
        )

        quad = np.array([
            -0.5, -0.5,  0.0, 0.0,
             0.5, -0.5,  1.0, 0.0,
             0.5,  0.5,  1.0, 1.0,
            -0.5,  0.5,  0.0, 1.0,
        ], dtype='f4')

        self.vbo = self.ctx.buffer(quad.tobytes())
        self.vao = self.ctx.simple_vertex_array(
            self.prog, self.vbo, 'in_pos', 'in_uv'
        )


    def get_keyboard_input(self):
        pressed_keys = {}
        for key_code in range(0, 350):
            state = glfw.get_key(self.window, key_code)
            pressed_keys[key_code] = state == glfw.PRESS
        return pressed_keys

    def get_events(self):
        events = set()

        if glfw.window_should_close(self.window):
            events.add(Event.QUIT)

        return events



    def process_image(self, image_id, scalex, scaley, rotation, alpha, cache_id):
        # GPU handles scale/rotation → just cache ID
        self.images[cache_id] = (image_id, scalex, scaley, rotation, alpha)



    def schedule_draw_text(self, *args, **kwargs):
        pass




    def schedule_blit(self, image_id, position, rotation, scalex, scaley, alpha,
                      layer, camera, always_render, cache_id, is_dirty, is_overlay):

        image = self.preprocessed_images.get(image_id)
        if image is None:
            return

        width, height = image

        if not check_on_screen(position, width * scalex, height * scaley, camera) \
           and not always_render and not is_overlay:
            return
        

        if cache_id not in self.images or is_dirty:
            self.process_image(image_id, scalex, scaley, rotation, alpha, cache_id)

        if not is_overlay:
            screen_x = position[0] - camera.transform.x
            screen_y = position[1] - camera.transform.y
        else:
            screen_x = position[0]
            screen_y = position[1]

        self.blit_schedule.append((
            cache_id,
            (screen_x, screen_y),
            layer
        ))



    def blit(self):
        self.blit_schedule.sort(key=lambda x: x[2])

        for cache_id, position, _ in self.blit_schedule:
            image_id, sx, sy, rotation, alpha = self.images[cache_id]
            tex = self.textures[image_id]


            tex.use()

            x = (position[0] / self.width) * 2 - 1
            y = (position[1] / self.height) * 2 - 1

            self.prog['offset'].value = (x, y)
            self.prog['scale'].value = (
                (sx * tex.width) / self.width * 2,
                (sy * tex.height) / self.height * 2
            )


            self.vao.render(moderngl.TRIANGLE_FAN)

        self.blit_schedule.clear()


    def schedule_draw_polygon(self, *args, **kwargs):
        pass 

    def schedule_draw_circle(self, *args, **kwargs):
        pass

    def draw_debug_shapes(self):
        self.draw_schedule.clear()



    def clear_screen(self):
        self.ctx.clear(0.0, 0.0, 0.0)

    def update_screen(self):
        glfw.swap_buffers(self.window)


    def load_image(self, path, image_id):
        try:
            img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert("RGBA")
            tex = self.ctx.texture(img.size, 4, img.tobytes())
            tex.build_mipmaps()

            self.textures[image_id] = tex
            self.preprocessed_images[image_id] = img.size

        except Exception as e:
            error(f"Error loading image '{path}': {e}.")