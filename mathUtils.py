import math

from pygame import Vector2

class fMath:
    @staticmethod
    def normalize(vec):
        x, y = vec
        length = math.sqrt(x * x + y * y)
        if length == 0:
            return (0.0, 0.0)
        return (x / length, y / length)

    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * t

    @staticmethod
    def dot(v1, v2):
        return v1[0] * v2[0] + v1[1] * v2[1]

    @staticmethod
    def cross(v1, v2):
        return v1[0] * v2[1] - v1[1] * v2[0]

    @staticmethod
    def distance(p1, p2):
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    def angle_between(v1, v2):
        dot_prod = fMath.dot(v1, v2)
        len1 = math.sqrt(v1[0] * v1[0] + v1[1] * v1[1])
        len2 = math.sqrt(v2[0] * v2[0] + v2[1] * v2[1])
        if len1 == 0 or len2 == 0:
            return 0.0
        cos_theta = dot_prod / (len1 * len2)
        cos_theta = max(-1.0, min(1.0, cos_theta))
        return math.acos(cos_theta)

    @staticmethod
    def rotate(vec, angle):
        x, y = vec
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)

    @staticmethod
    def almost_equal(a, b, epsilon=1e-6):
        return abs(a - b) < epsilon

    @staticmethod
    def clamp(value, min_val, max_val):
        return max(min_val, min(value, max_val))

    @staticmethod
    def remap(value, in_min, in_max, out_min, out_max):
        if in_max == in_min:
            raise ValueError("Input range cannot be zero.")
        return out_min + (float(value - in_min) / float(in_max - in_min)) * (out_max - out_min)


    @staticmethod
    def wrap(value, min_val, max_val):
        if min_val >= max_val:
            raise ValueError("min_val must be less than max_val.")
        range_size = max_val - min_val
        return ((value - min_val) % range_size) + min_val

    class Vector2:
        __slots__ = ("x", "y")

        def __init__(self, x=0.0, y=0.0):
            self.x = float(x)
            self.y = float(y)

        # ---------- String ----------

        def __repr__(self):
            return f"Vector2({self.x}, {self.y})"

        def __str__(self):
            return f"({self.x}, {self.y})"

        # ---------- Arithmetic ----------

        def __add__(self, other):
            return fMath.Vector2(self.x + other.x, self.y + other.y)

        def __sub__(self, other):
            return fMath.Vector2(self.x - other.x, self.y - other.y)

        def __mul__(self, value):
            if isinstance(value, fMath.Vector2):
                return fMath.Vector2(self.x * value.x, self.y * value.y)
            return fMath.Vector2(self.x * value, self.y * value)

        def __rmul__(self, value):
            return self * value

        def __truediv__(self, value):
            if isinstance(value, fMath.Vector2):
                return fMath.Vector2(self.x / value.x, self.y / value.y)
            return fMath.Vector2(self.x / value, self.y / value)

        def __neg__(self):
            return fMath.Vector2(-self.x, -self.y)

        # ---------- In-place ----------

        def __iadd__(self, other):
            self.x += other.x
            self.y += other.y
            return self

        def __isub__(self, other):
            self.x -= other.x
            self.y -= other.y
            return self

        def __imul__(self, value):
            self.x *= value
            self.y *= value
            return self

        def __itruediv__(self, value):
            self.x /= value
            self.y /= value
            return self

        # ---------- Comparison ----------

        def __eq__(self, other):
            if not isinstance(other, fMath.Vector2):
                return False
            return self.x == other.x and self.y == other.y

        # ---------- Indexing ----------

        def __getitem__(self, index):
            if index == 0:
                return self.x
            elif index == 1:
                return self.y
            raise IndexError("Vector2 index out of range")

        def __setitem__(self, index, value):
            if index == 0:
                self.x = value
            elif index == 1:
                self.y = value
            else:
                raise IndexError("Vector2 index out of range")

        # ---------- Utilities ----------

        def copy(self):
            return fMath.Vector2(self.x, self.y)

        def to_tuple(self):
            return (self.x, self.y)

        # ---------- Magnitude ----------

        @property
        def magnitude(self):
            return math.sqrt(self.x * self.x + self.y * self.y)

        @property
        def magnitude_squared(self):
            return self.x * self.x + self.y * self.y

        def length(self):
            return self.magnitude

        def length_squared(self):
            return self.magnitude_squared

        # ---------- Normalization ----------

        def normalize(self):
            mag = self.magnitude
            if mag == 0:
                return fMath.Vector2()
            return self / mag

        def normalized(self):
            return self.normalize()

        # ---------- Vector Math ----------

        def dot(self, other):
            return self.x * other.x + self.y * other.y

        def distance_to(self, other):
            return (other - self).magnitude

        def angle(self):
            return math.atan2(self.y, self.x)

        def angle_to(self, other):
            return math.atan2(other.y - self.y, other.x - self.x)

        def rotate(self, radians):
            c = math.cos(radians)
            s = math.sin(radians)

            return fMath.Vector2(
                self.x * c - self.y * s,
                self.x * s + self.y * c
            )

        def lerp(self, other, t):
            return self + (other - self) * t

        def clamp(self, max_length):
            if self.magnitude > max_length:
                return self.normalize() * max_length
            return self.copy()

        # ---------- Static Constructors ----------

        @staticmethod
        def zero():
            return fMath.Vector2(0, 0)

        @staticmethod
        def one():
            return fMath.Vector2(1, 1)

        @staticmethod
        def up():
            return fMath.Vector2(0, -1)

        @staticmethod
        def down():
            return fMath.Vector2(0, 1)

        @staticmethod
        def left():
            return fMath.Vector2(-1, 0)

        @staticmethod
        def right():
            return fMath.Vector2(1, 0)