class Object:
    def __init__(self, engine):
        self.engine = engine
        self.transform = None
        self.renderer = None
        self.script = None
        self.collider = None
        self.camera = None
        self.textRenderer = None
        self.audio = None
        self.tags = []

    def update(self):
        if self.script and hasattr(self.script, 'update'):
            self.script.update(thisObject=self, engine=self.engine)

    def add_audio(self, audio_component):
        self.audio.append(audio_component)

    def has_tag(self, tag):
        return tag in self.tags

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def remove_tag(self, tag):
        if tag in self.tags:
            self.tags.remove(tag)

    def start(self):
        if self.script and hasattr(self.script, 'start'):
            self.script.start(thisObject=self, engine=self.engine)

    def early_update(self):
        if self.script and hasattr(self.script, 'EarlyUpdate'):
            self.script.EarlyUpdate(thisObject=self, engine=self.engine)