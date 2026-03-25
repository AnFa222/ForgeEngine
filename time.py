class Time:
    def __init__(self):
        self.delta_time = 0.0
        self.timers = {}

    def update(self, delta_time):
        self.deltaTime = delta_time
        for id in self.timers:
            self.timers[id] += self.deltaTime

    def create_timer(self, id):
        if id not in self.timers:
            self.timers[id] = 0.0
        
    def reset_timer(self, id):
        if id in self.timers:
            self.timers[id] = 0.0

    def get_timer(self, id):
        return self.timers.get(id, None)