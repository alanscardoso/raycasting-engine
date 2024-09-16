import glfw
from OpenGL.GL import *

glfw.init()
window = glfw.create_window(640, 480, "Raycasting Engine", None, None)
glfw.make_context_current(window)    

def draw_player(x, y):
    glPointSize(8)
    glColor3f(1, 1, 0)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

while not glfw.window_should_close(window):
    glClearColor(0.0, 0.0, 0.0, 1)
    glClear(GL_COLOR_BUFFER_BIT)

    draw_player(0, 0)

    glfw.swap_buffers(window)
    glfw.poll_events()

glfw.terminate()