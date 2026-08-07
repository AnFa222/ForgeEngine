from .log import error

class Animation:
    def __init__(self, frame_ids, frame_duration=0.1, loop=True, playing=True):
        self.frame_ids = list(frame_ids) if frame_ids else []
        self.frame_duration = frame_duration
        self.loop = loop
        self.playing = playing
        self.current_frame = 0
        self.elapsed_time = 0.0

    def update(self, delta_time):
        if not self.playing or len(self.frame_ids) == 0:
            return

        self.elapsed_time += delta_time
        while self.elapsed_time >= self.frame_duration:
            self.elapsed_time -= self.frame_duration
            self.current_frame += 1
            if self.current_frame >= len(self.frame_ids):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frame_ids) - 1
                    self.playing = False
                    break

    def get_current_frame(self):
        if len(self.frame_ids) == 0:
            return None
        return self.frame_ids[self.current_frame]

    def play(self):
        self.playing = True

    def pause(self):
        self.playing = False

    def stop(self):
        self.playing = False
        self.current_frame = 0
        self.elapsed_time = 0.0

    def reset(self):
        self.current_frame = 0
        self.elapsed_time = 0.0
