class Audio:
    def __init__(self, audio_id):
        self.audio_id = audio_id
        self.play = False
        self.stop = False
    
    def play_sound(self):
        self.play = True

    def stop_sound(self):
        self.stop = True