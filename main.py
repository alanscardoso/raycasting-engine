import math
import glfw
from OpenGL.GL import *

width = 512
height = 512
player_x = 0
player_y = 0
player_speed = 2
player_rotation = 0 # degrees
rotation_speed = 2
square_size = 64
map_side = 8

# raycasting parameters
fov = 60
num_rays = width // 2 # we can cast one ray every 2 pixels to get a good resolution without too much performance cost
ray_col_width = 2
max_depth = square_size * map_side # max distance a ray can travel
step_size = 4 # how much distance we advance each ray check

glfw.init()
glfw.window_hint(glfw.RESIZABLE, glfw.FALSE)
window = glfw.create_window(width, height, "Raycasting Engine", None, None)
glfw.make_context_current(window)    

# TODO extract map information to other file and load into here
# all maps should be squaresXsquares size
map_2d = [
    1,1,1,1,1,1,1,1,
    1,0,0,0,0,0,0,1,
    1,0,1,1,0,0,0,1,
    1,0,1,0,0,1,0,1,
    1,0,1,0,0,1,0,1,
    1,0,0,0,1,1,0,1,
    1,0,0,0,0,0,0,1,
    1,1,1,1,1,1,1,1,
]

# here we ensure player will never start in a wall
# player will start in center of the firt top-left square free
def set_player_start_point():
    global map_2d, square_size, map_side, player_x, player_y

    x, y = 0, square_size*7

    count = 0
    for i in map_2d:
        if i == 0:
            player_x = x + int(square_size/2)
            player_y = y + int(square_size/2)

            return True
        
        x += square_size
        count += 1

        if count == map_side:
            count = 0
            y -= square_size
            x = 0

    return False

def is_wall_collision(player_x, player_y):
    global map_2d, square_size, map_side

    x, y = 0, square_size*7

    count = 0
    for i in map_2d:
        vertex_0 = (x, y)
        vertex_2 = (x + square_size, y + square_size) 

        if player_x >= vertex_0[0] and player_x <= vertex_2[0]:
            if player_y >= vertex_0[1] and player_y <= vertex_2[1]:
                if i == 1:
                    return True

        x += square_size
        count += 1

        if count == map_side:
            count = 0
            y -= square_size
            x = 0

    return False

# TODO must be a best way of drawing the map
def draw_2d_map():
    global map_2d, square_size, map_side

    scale = 0.3
    x, y = 0, (square_size*7) * scale

    count = 0
    for i in map_2d:
        if i == 0: 
            glColor3f(0,0,0)
        if i == 1:
            glColor3f(1,1,1)

        sx = x
        sy = y
        ss = square_size * scale

        # the vertices must be draw in clockwise order
        glBegin(GL_QUADS)
        glVertex2f(sx + 1, sy + 1)
        glVertex2f(sx + ss - 1, sy + 1)
        glVertex2f(sx + ss - 1, sy + ss - 1)
        glVertex2f(sx + 1, sy + ss - 1)
        glEnd()

        x += square_size * scale
        count += 1

        if count == map_side:
            count = 0
            y -= square_size * scale
            x = 0

# change the center relative to a pixel base system to draw stuff
def setup_projection():
    width, height = glfw.get_framebuffer_size(window)

    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

def draw_player():
    global player_x, player_y, player_rotation, square_size
    scale = 0.3

    px = player_x * scale
    py = player_y * scale

    glPointSize(8)
    glColor3f(1, 1, 0)
    glBegin(GL_POINTS)
    glVertex2i(int(px), int(py))
    glEnd()

    radian_angle = math.radians(player_rotation)
    line_length = 30 * scale

    line_end_x = px + line_length * math.cos(radian_angle)
    line_end_y = py + line_length * math.sin(radian_angle)

    glLineWidth(2)
    glColor3f(1, 0, 0)
    glBegin(GL_LINES)
    glVertex2f(px, py)
    glVertex2f(line_end_x, line_end_y)
    glEnd()

def player_movement():
    global player_x, player_y, player_speed, player_rotation, rotation_speed
    width, height = glfw.get_framebuffer_size(window)

    radian_angle = math.radians(player_rotation)
    
    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        new_x = player_x + player_speed * math.cos(radian_angle)
        new_y = player_y + player_speed * math.sin(radian_angle)
        if not is_wall_collision(new_x, new_y):
            player_x = new_x
            player_y = new_y

    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        new_x = player_x - player_speed * math.cos(radian_angle)
        new_y = player_y - player_speed * math.sin(radian_angle)
        if not is_wall_collision(new_x, new_y):
            player_x = new_x
            player_y = new_y

    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        player_rotation += rotation_speed

    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        player_rotation -= rotation_speed

    if player_x < 0:
        player_x = 0
    if player_x > width:
        player_x = width
    if player_y < 0:
        player_y = 0
    if player_y > height:
        player_y = height

    player_rotation %= 360

def cast_rays_and_draw_3d():
    global player_x, player_y, player_rotation, fov, num_rays, max_depth, step_size

    start_angle = player_rotation - (fov / 2)
    angle_step = fov / num_rays

    for ray in range(num_rays):
        current_angle_deg = start_angle + ray * angle_step
        current_angle_rad = math.radians(current_angle_deg)

        # step forward until hit wall or max depth
        distance = 0
        hit_wall = False

        while distance < max_depth:
            test_x = player_x + math.cos(current_angle_rad) * distance
            test_y = player_y + math.sin(current_angle_rad) * distance

            if is_wall_collision(test_x, test_y):
                hit_wall = True
                break

            distance += step_size

        if not hit_wall:
            continue

        # fix fish-eye: project the distance to player's view direction
        delta_angle = math.radians(current_angle_deg - player_rotation)
        distance_corrected = distance * math.cos(delta_angle)

        if distance_corrected == 0:
            distance_corrected = 0.0001

        wall_height = (square_size * height) / distance_corrected

        # center the wall vertically
        wall_top = (height / 2) - (wall_height / 2)
        wall_bottom = wall_top + wall_height

        if wall_top < 0:
            wall_top = 0
        if wall_bottom > height:
            wall_bottom = height

        # shading: farther walls darker
        shade = 1.0 - min(distance_corrected / max_depth, 1.0)
        glColor3f(shade, shade, shade)

        # draw vertical line for this ray
        screen_x = ray * ray_col_width
        glBegin(GL_LINES)
        glVertex2f(screen_x, int(wall_top))
        glVertex2f(screen_x, int(wall_bottom))
        glVertex2f(screen_x + ray_col_width, int(wall_top))
        glVertex2f(screen_x + ray_col_width, int(wall_bottom))
        glVertex2f(screen_x, int(wall_bottom))
        glEnd()

set_player_start_point() 

while not glfw.window_should_close(window):
    setup_projection()

    glClearColor(0.5, 0.5, 0.5, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    cast_rays_and_draw_3d()
    player_movement()
    draw_2d_map()
    draw_player()

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()