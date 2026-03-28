class Kinematic:
    def __init__(self):
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self, thisObject, engine):
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