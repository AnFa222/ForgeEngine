from .log import error

class Scene:
    def __init__(self, scene_id):
        self.scene_id = scene_id
        self.background_color = (0, 0, 0)
        self.objects = []
        self.objects_to_destroy = []

    def add_object(self, obj):
        self.objects.append(obj)

    def destroy_object(self, obj):
        if obj in self.objects:
            self.objects_to_destroy.append(obj)
        else:
            error(f"Attempted to destroy and invalid object {obj}.")