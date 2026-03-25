class Camera:
    def __init__(self, camera_id):
        self.camera_id = camera_id
        self.render_zone_width = None
        self.render_zone_height = None
        self.render_zone_offset_x = 0
        self.render_zone_offset_y = 0