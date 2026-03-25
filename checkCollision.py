from .objectComponents.colliderComponent import Rectangle, Polygon
import math



def get_collider_center(obj, collider):
    ox = collider.x_offset
    oy = collider.y_offset
    angle = math.radians(obj.transform.rotation)
    cos_r = math.cos(angle)
    sin_r = math.sin(angle)
    rx = ox * cos_r - oy * sin_r
    ry = ox * sin_r + oy * cos_r
    return obj.transform.x + rx, obj.transform.y + ry


def get_rect_corners(obj, collider):
    cx, cy = get_collider_center(obj, collider)

    w = collider.shape.width * obj.transform.scale_x
    h = collider.shape.height * obj.transform.scale_y

    angle = math.radians(-obj.transform.rotation) 
    cos_r = math.cos(angle)
    sin_r = math.sin(angle)

    hw = w / 2
    hh = h / 2

    corners = [
        (-hw, -hh),
        ( hw, -hh),
        ( hw,  hh),
        (-hw,  hh)
    ]

    rotated = []
    for x, y in corners:
        rx = x * cos_r - y * sin_r + cx
        ry = x * sin_r + y * cos_r + cy
        rotated.append((rx, ry))

    return rotated


def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]


def cross_product(a, b):
    return a[0] * b[1] - a[1] * b[0]


def is_convex_polygon(points):
    """Check if polygon is convex using cross product method"""
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

        cross = cross_product(v1, v2)

        if cross != 0: 
            if sign is None:
                sign = cross > 0
            elif (cross > 0) != sign:
                return False

    return True


def validate_polygon_convexity(points):
    """Runtime function to validate polygon convexity - raises ValueError if not convex"""
    if not is_convex_polygon(points):
        raise ValueError("Polygon is not convex - only convex polygons are supported for collision detection")


def get_polygon_world_points(obj, collider):
    """Get polygon points transformed to world space"""
    cx, cy = get_collider_center(obj, collider)

    angle = math.radians(-obj.transform.rotation) 
    cos_r = math.cos(angle)
    sin_r = math.sin(angle)
    scale_x = obj.transform.scale_x
    scale_y = obj.transform.scale_y

    world_points = []
    for px, py in collider.shape.points:
        scaled_x = px * scale_x
        scaled_y = py * scale_y

        rx = scaled_x * cos_r - scaled_y * sin_r
        ry = scaled_x * sin_r + scaled_y * cos_r

        world_points.append((cx + rx, cy + ry))

    return world_points


def polygon_vs_polygon(obj1, obj2, c1, c2):
    points1 = get_polygon_world_points(obj1, c1)
    points2 = get_polygon_world_points(obj2, c2)

    axes = get_axes(points1) + get_axes(points2)

    for axis in axes:
        p1 = project(points1, axis)
        p2 = project(points2, axis)

        if not overlap(p1, p2):
            return False

    return True


def get_axes(corners):
    axes = []
    for i in range(len(corners)):
        p1 = corners[i]
        p2 = corners[(i + 1) % len(corners)]

        edge = (p2[0] - p1[0], p2[1] - p1[1])
        normal = (-edge[1], edge[0]) 

        length = math.hypot(normal[0], normal[1])
        axes.append((normal[0]/length, normal[1]/length))

    return axes


def project(corners, axis):
    dots = [dot(c, axis) for c in corners]
    return min(dots), max(dots)


def overlap(p1, p2):
    return p1[0] <= p2[1] and p2[0] <= p1[1]


def rect_vs_rect(obj1, obj2, c1, c2):
    corners1 = get_rect_corners(obj1, c1)
    corners2 = get_rect_corners(obj2, c2)

    axes = get_axes(corners1) + get_axes(corners2)

    for axis in axes:
        p1 = project(corners1, axis)
        p2 = project(corners2, axis)

        if not overlap(p1, p2):
            return False

    return True



def check_collision_pair(obj1, obj2):
    c1 = obj1.collider
    c2 = obj2.collider

    if not c1 or not c2:
        return False

    if isinstance(c1.shape, Rectangle) and isinstance(c2.shape, Rectangle):
        return rect_vs_rect(obj1, obj2, c1, c2)

    elif isinstance(c1.shape, Polygon) and isinstance(c2.shape, Polygon):
        if not is_convex_polygon(c1.shape.points):
            raise ValueError("Polygon 1 is not convex")
        if not is_convex_polygon(c2.shape.points):
            raise ValueError("Polygon 2 is not convex")
        return polygon_vs_polygon(obj1, obj2, c1, c2)

    elif (isinstance(c1.shape, Rectangle) and isinstance(c2.shape, Polygon)) or \
         (isinstance(c1.shape, Polygon) and isinstance(c2.shape, Rectangle)):

        if isinstance(c1.shape, Rectangle):
            rect_obj, poly_obj = obj1, obj2
            r, p = c1, c2
        else:
            rect_obj, poly_obj = obj2, obj1
            r, p = c2, c1

        rect_points = get_rect_corners(rect_obj, r)
        poly_points = get_polygon_world_points(poly_obj, p)

        axes = get_axes(rect_points) + get_axes(poly_points)

        for axis in axes:
            p1 = project(rect_points, axis)
            p2 = project(poly_points, axis)

            if not overlap(p1, p2):
                return False

        return True

    else:
        raise ValueError("Unsupported shape combination")




def check_collision_all(obj, objects):
    collisions = []

    for other in objects:
        if other is obj:
            continue

        if check_collision_pair(obj, other):
            collisions.append(other)

    return collisions