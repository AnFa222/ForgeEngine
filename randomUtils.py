import random
import math

def random_range(min_val, max_val, seed=None):
    if seed is not None:
        random.seed(seed)
    return random.uniform(min_val, max_val)

def random_int(min_val, max_val, seed=None):
    if seed is not None:
        random.seed(seed)
    return random.randint(min_val, max_val)

def random_choice(seq, seed=None):
    if seed is not None:
        random.seed(seed)
    return random.choice(seq)

def random_bool(prob=0.5, seed=None):
    if seed is not None:
        random.seed(seed)
    return random.random() < prob


def random_unit_vector(seed=None):
    if seed is not None:
        random.seed(seed)
    angle = random.uniform(0, 2 * math.pi)
    return (math.cos(angle), math.sin(angle))

def random_in_rect(x, y, w, h, seed=None):
    if seed is not None:
        random.seed(seed)
    return (random.uniform(x, x + w), random.uniform(y, y + h))

def random_in_circle(center, radius, seed=None):
    if seed is not None:
        random.seed(seed)
    angle = random.uniform(0, 2 * math.pi)
    r = radius * math.sqrt(random.random())
    return (center[0] + r * math.cos(angle), center[1] + r * math.sin(angle))

def jitter(value, amount, seed=None):
    if seed is not None:
        random.seed(seed)
    return value + random.uniform(-amount, amount)

def weighted_choice(choices, seed=None):
    if seed is not None:
        random.seed(seed)
    total = sum(weight for _, weight in choices)
    r = random.uniform(0, total)
    upto = 0
    for item, weight in choices:
        if upto + weight >= r:
            return item
        upto += weight
    return choices[-1][0]

# Perlin Noise
def _grad(hash_val, x, y=0):
    h = hash_val & 3
    if h == 0: return x + y
    if h == 1: return -x + y
    if h == 2: return x - y
    return -x - y

def _fade(t):
    return t * t * t * (t * (t * 6 - 15) + 10)

def _lerp(a, b, t):
    return a + t * (b - a)

def _make_perm(seed=None):
    perm = list(range(256))
    if seed is not None:
        random.seed(seed)
    random.shuffle(perm)
    return perm + perm

_perm = _make_perm()

def perlin1d(x, seed=None):
    global _perm
    if seed is not None:
        _perm = _make_perm(seed)

    xi = int(math.floor(x)) & 255
    xf = x - math.floor(x)
    u = _fade(xf)

    a = _perm[xi]
    b = _perm[xi + 1]

    return _lerp(_grad(a, xf), _grad(b, xf - 1), u)

def perlin2d(x, y, seed=None):
    global _perm
    if seed is not None:
        _perm = _make_perm(seed)

    xi = int(math.floor(x)) & 255
    yi = int(math.floor(y)) & 255
    xf = x - math.floor(x)
    yf = y - math.floor(y)
    u = _fade(xf)
    v = _fade(yf)

    aa = _perm[_perm[xi] + yi]
    ab = _perm[_perm[xi] + yi + 1]
    ba = _perm[_perm[xi + 1] + yi]
    bb = _perm[_perm[xi + 1] + yi + 1]

    x1 = _lerp(_grad(aa, xf, yf), _grad(ba, xf - 1, yf), u)
    x2 = _lerp(_grad(ab, xf, yf - 1), _grad(bb, xf - 1, yf - 1), u)

    return _lerp(x1, x2, v)
