import math

def normalize(vec):
    x, y = vec
    length = math.sqrt(x * x + y * y)
    if length == 0:
        return (0.0, 0.0)
    return (x / length, y / length)

def lerp(a, b, t):
    return a + (b - a) * t

def dot(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]

def cross(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def distance(p1, p2):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    return math.sqrt(dx * dx + dy * dy)

def angle_between(v1, v2):
    dot_prod = dot(v1, v2)
    len1 = math.sqrt(v1[0] * v1[0] + v1[1] * v1[1])
    len2 = math.sqrt(v2[0] * v2[0] + v2[1] * v2[1])
    if len1 == 0 or len2 == 0:
        return 0.0
    cos_theta = dot_prod / (len1 * len2)
    cos_theta = max(-1.0, min(1.0, cos_theta))
    return math.acos(cos_theta)

def rotate(vec, angle):
    x, y = vec
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)

def almost_equal(a, b, epsilon=1e-6):
    return abs(a - b) < epsilon

def clamp(value, min_val, max_val):
    return max(min_val, min(value, max_val))


def remap(value, in_min, in_max, out_min, out_max):
    if in_max == in_min:
        raise ValueError("Input range cannot be zero.")
    return out_min + (float(value - in_min) / float(in_max - in_min)) * (out_max - out_min)


def wrap(value, min_val, max_val):
    if min_val >= max_val:
        raise ValueError("min_val must be less than max_val.")
    range_size = max_val - min_val
    return ((value - min_val) % range_size) + min_val
