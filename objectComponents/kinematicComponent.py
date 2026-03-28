import math

class Kinematic:
    def __init__(self):
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0
        self.gravity_direction = 0
        self.friction = 0

    def update(self, thisObject, engine):
        self.velocity_x += self.gravity * math.cos(math.radians(self.gravity_direction)) * engine.deltaTime
        self.velocity_y += self.gravity * math.sin(math.radians(self.gravity_direction)) * engine.deltaTime
        self.velocity_x -= self.friction * self.velocity_x * engine.deltaTime
        self.velocity_y -= self.friction * self.velocity_y * engine.deltaTime

        if not thisObject.collider:
            thisObject.transform.x += self.velocity_x * engine.deltaTime
            thisObject.transform.y += self.velocity_y * engine.deltaTime
            return

        dt = engine.deltaTime
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
            thisObject.transform.y = original_y
            self.velocity_y = 0 