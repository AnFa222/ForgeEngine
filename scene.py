class Scene:
    def __init__(self, scene_id):
        self.scene_id = scene_id
        self.background_color = (0, 0, 0)
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)