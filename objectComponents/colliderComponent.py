from .log import error

class Collider:
    def __init__(self, shape, x_offset, y_offset):
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.shape = shape

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

class Polygon:
    def __init__(self, points):
        if not self._is_convex(points):
            error("Polygon is not convex. Switching to dot colider.")
            self.points = [(0,0),(0.1,0.1),(0.1,0)]
        else:
            self.points = points

    @staticmethod
    def _is_convex(points):
        if len(points) < 3:
            return False

        sign = None
        n = len(points)

        for i in range(n):
            p1 = points[i]
            p2 = points[(i + 1) % n]
            p3 = points[(i + 2) % n]

            v1 = (p2[0] - p1[0], p2[1] - p1[1])
            v2 = (p3[0] - p2[0], p3[1] - p2[1])

            cross = v1[0] * v2[1] - v1[1] * v2[0]

            if cross != 0:
                if sign is None:
                    sign = cross > 0
                elif (cross > 0) != sign:
                    return False

        return True