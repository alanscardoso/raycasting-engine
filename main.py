import glfw
from OpenGL.GL import *

width = 640
height = 480
player_x = 320
player_y = 240
player_speed = 1

glfw.init()
window = glfw.create_window(width, height, "Raycasting Engine", None, None)
glfw.make_context_current(window)    

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
    global width, height, player_x, player_y

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

    glClearColor(0.0, 0.0, 0.0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    player_movement()  
    draw_player(player_x, player_y)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()