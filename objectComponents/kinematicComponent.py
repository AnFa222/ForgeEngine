import math

class Kinematic:
    def __init__(self):
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0
        self.gravity_direction = 90
        self.friction = 0
        self.on_ground = False 

    def update(self, thisObject, engine):
        dt = engine.deltaTime

        if not self.on_ground:
            self.velocity_x += self.gravity * math.cos(math.radians(self.gravity_direction)) * dt
            self.velocity_y += self.gravity * math.sin(math.radians(self.gravity_direction)) * dt

        self.velocity_x -= self.friction * self.velocity_x * dt
        self.velocity_y -= self.friction * self.velocity_y * dt

        if not thisObject.collider:
            thisObject.transform.x += self.velocity_x * dt
            thisObject.transform.y += self.velocity_y * dt
            return

        original_x = thisObject.transform.x
        original_y = thisObject.transform.y

        thisObject.transform.x += self.velocity_x * dt
        collisions_x = engine.check_collision(thisObject, engine.objects)
        if collisions_x:
            thisObject.transform.x = original_x
            self.velocity_x = 0

        thisObject.transform.y += self.velocity_y * dt
        collisions_y = engine.check_collision(thisObject, engine.objects)
        if collisions_y:
            self.on_ground = True
            thisObject.transform.y = original_y
            self.velocity_y = 0
        else:
            self.on_ground = False