import glfw
from OpenGL.GL import *

width = 512
height = 512
player_x = 256
player_y = 256
player_speed = 2

glfw.init()
window = glfw.create_window(width, height, "Raycasting Engine", None, None)
glfw.make_context_current(window)    


def draw_2d_map():
    square_size = 64
    x, y = 0, square_size*7

    map2d = [
        1,1,1,1,1,1,1,1,
        1,0,0,0,0,0,0,1,
        1,0,1,0,0,0,0,1,
        1,0,1,1,0,1,0,1,
        1,0,1,0,1,1,0,1,
        1,0,0,0,0,1,0,1,
        1,0,0,0,0,0,0,1,
        1,1,1,1,1,1,1,1,
    ]

    count = 0
    for i in map2d:
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

        if count == 8:
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

def draw_player(x, y):
    glPointSize(8)
    glColor3f(1, 1, 0)
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()

def player_movement():
    global player_x, player_y
    width, height = glfw.get_framebuffer_size(window)

    if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
        player_y += player_speed 
    if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
        player_y -= player_speed
    if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
        player_x -= player_speed
    if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
        player_x += player_speed

    if player_x < 0: 
        player_x = 0
    if player_x > width:
        player_x = width
    if player_y < 0: 
        player_y = 0
    if player_y > height:
        player_y = height
    

while not glfw.window_should_close(window):
    setup_projection()

    glClearColor(0.5, 0.5, 0.5, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    draw_2d_map()

    player_movement()  
    draw_player(player_x, player_y)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()