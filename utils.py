def check_on_screen(position, width, height, camera):
    camera_render_zone_width = camera.camera.render_zone_width
    camera_render_zone_height = camera.camera.render_zone_height
    camera_render_zone_offset_x = camera.camera.render_zone_offset_x
    camera_render_zone_offset_y = camera.camera.render_zone_offset_y

    screen_x = position[0] - width / 2 - camera.transform.x
    screen_y = position[1] - height / 2 - camera.transform.y

    if (screen_x + width < -camera_render_zone_offset_x or
        screen_x > camera_render_zone_width - camera_render_zone_offset_x or
        screen_y + height < -camera_render_zone_offset_y or
        screen_y > camera_render_zone_height - camera_render_zone_offset_y):
        return False

    return True