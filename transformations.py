import math

#UNSUSED CODE FOR CAMERA ROTATION. FEATURE UNDER DEVELOPMENT

def rotate(point, center, angle):
    sin_angle = math.sin(angle)
    cos_angle = math.cos(angle)
    translated_x = point[0] - center[0]
    translated_y = point[1] - center[1]
    rotated_x = translated_x * cos_angle - translated_y * sin_angle
    rotated_y = translated_x * sin_angle + translated_y * cos_angle
    return (rotated_x + center[0], rotated_y + center[1])