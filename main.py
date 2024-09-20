import math
import glfw
from OpenGL.GL import *

width = 512
height = 512
player_x = 0
player_y = 0
player_speed = 2
player_rotation = 0
rotation_speed = 2

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
    x, y = 0, square_size*7

    count = 0
    for i in map_2d:
        if i == 0: 
            glColor3f(0,0,0)
        if i == 1:
            glColor3f(1,1,1)

        # the vertices must be draw in clockwise order
        glBegin(GL_QUADS)
        glVertex2i(x + 1, y + 1)
        glVertex2i(x + square_size - 1, y + 1)
        glVertex2i(x + square_size - 1, y + square_size - 1)
        glVertex2i(x + 1, y + square_size - 1)
        glEnd()

        x += square_size
        count += 1

        if count == map_side:
            count = 0
            y -= square_size
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
    global player_x, player_y, player_rotation

    glPointSize(8)
    glColor3f(1, 1, 0)
    glBegin(GL_POINTS)
    glVertex2i(int(player_x), int(player_y))
    glEnd()

    radian_angle = math.radians(player_rotation)
    line_length = 30

    line_end_x = player_x + line_length * math.cos(radian_angle)
    line_end_y = player_y + line_length * math.sin(radian_angle)

    glLineWidth(2)
    glColor3f(1, 0, 0)
    glBegin(GL_LINES)
    glVertex2i(int(player_x), int(player_y))
    glVertex2i(int(line_end_x), int(line_end_y))
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


set_player_start_point() 

while not glfw.window_should_close(window):
    setup_projection()

    glClearColor(0.5, 0.5, 0.5, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    draw_2d_map()

    player_movement()  
    draw_player()

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()